from random import randint

from flask import jsonify, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required

from app import app, BOTINDER_API_URL, BOTINDER_API_HEADERS
from app.forms.forms import AdminForm
from app.models.matches import RobotMatches, UnMatches, UserMatches
from app.models.robots import RobotProfile, UserRobot
from app.services.database_operations.database_operations import (
    add_chatroom, add_match_unmatch, add_message_to_chatroom, delete_chatroom,
    delete_matched_pair, get_chatroom_messages, get_matched_robots,
    get_not_matched_robots_by_localization, get_robot_info_by_chatroom_id,
    get_single_matched_robot, get_user, insert_into_robots_db,
    select_all_from_database, session_scope, update_user_location,
    update_user_location_domicile)
from app.services.API_requests.requests import get_botinderAPI_coordinates
from app.services.database_operations.robots_generator.generate_robots import \
    generate_random_robots
from app.services.geolocalization_services.user_localization_and_distance import \
    get_coordinates, distance
from app.services.helpers import generate_robots, robot_to_dict
from app.services.robot_match.robot_selector import get_robots_for_user
from app.services.tasks.tasks import calL_GPT_API
from app.services.API_requests.requests import get_botinderAPI_coordinates, get_botinderAPI_distance

@app.route("/")
@app.route("/home")
def home():
    app.config['STATIC_USER_IP'] = request.remote_addr
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage"))
    else:
        return render_template("main/start-page.html")


@app.route("/lore")
def lore():
    return render_template("main/lore.html")


@app.route("/FAQ")
def FAQ():
        return render_template("main/FAQ.html")


@app.route("/user_homepage", methods=["GET"])
@login_required
def user_homepage():
    with session_scope() as session:
        robots_list = get_robots_for_user(current_user, session)
        if not robots_list:
            generate_robots(
                current_user=current_user, session=session, number_of_robots=5000
            )
            robots_list = get_robots_for_user(current_user, session)
        matched_robots = get_matched_robots(
            session, current_user.id, current_user.name, include_chatroom_id="yes"
        )
        return render_template(
            "user_homepage/user_homepage.html",
            user=current_user.username,
            robots_list=robot_to_dict(robots_list),
            matched_robots=matched_robots,
        )


@app.route("/unmatch", methods=["POST"])
@login_required
def unmatch():
    data = request.get_json()
    with session_scope() as session:
        add_match_unmatch(
            session,
            current_user.id,
            current_user.name,
            data["id"],
            data["name"],
            UnMatches,
        )

    return jsonify({"message": "Successfully matched"}), 200


@app.route("/match", methods=["POST"])
@login_required
def match():
    data = request.get_json()
    with session_scope() as session:
        add_match_unmatch(
            session,
            current_user.id,
            current_user.name,
            data["id"],
            data["name"],
            UserMatches,
        )

        random_match = randint(0, 2)
        if random_match == 1:
            add_match_unmatch(
                session,
                current_user.id,
                current_user.name,
                data["id"],
                data["name"],
                RobotMatches,
            )
            add_chatroom(session, current_user.id, data["id"])
            match_result = get_single_matched_robot(
                current_user.id, current_user.name, data["id"], session
            )
            robot_info = get_robot_info_by_chatroom_id(session, match_result[1])
            match_result_json = {
                "robot_image": robot_info.image_file,
                "chatroom_id": match_result[1],
                "robot_name": robot_info.name,
            }

            return (
                jsonify({"message": "Succes", "match_result": match_result_json}),
                200,
            )

    return jsonify({"message": "No match"}), 400


@app.route("/chatroom/<chatroom_id>")
@login_required
def chatroom(chatroom_id):
    with session_scope() as session:
        matched_robots = get_matched_robots(
            session, current_user.id, current_user.name, include_chatroom_id=True
        )
        robot_info = get_robot_info_by_chatroom_id(session, chatroom_id)
        chat_messages = get_chatroom_messages(session, chatroom_id)
        return render_template(
            "user_homepage/chatroom.html",
            chatroom_id=chatroom_id,
            user=current_user.username,
            matched_robots=matched_robots,
            robot_info=robot_info,
            messages=chat_messages,
        )


@app.route("/chatroom_unmatch", methods=["POST"])
@login_required
def chatroom_unmatch():
    data = request.get_json()
    chatroom_id = data.get("chatroomId")
    robot_name = data.get("robotName")
    user_name = data.get("userName")
    robot_id = data.get("robotId")

    with session_scope() as session:
        add_match_unmatch(
            session,
            current_user.id,
            current_user.name,
            robot_id,
            robot_name,
            UnMatches,  # data["name"] = robot_name
        )
        delete_chatroom(session, chatroom_id)
        delete_matched_pair(session, user_name, robot_name)
    return jsonify({"status": "success"})


@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        client_data = request.json

        GPT_response = calL_GPT_API()  # Załóżmy, że ta funkcja istnieje i działa.

        with session_scope() as session:
            add_message_to_chatroom(
                session, client_data["message"], client_data["chatroom_id"]
            )
            add_message_to_chatroom(
                session, GPT_response, client_data["chatroom_id"], "robot"
            )

        return jsonify({"message": GPT_response})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/get_robots", methods=["GET", "POST"])
@login_required
def get_robots():
    with session_scope() as session:
        robots_list = robot_to_dict(get_robots_for_user(current_user, session))
        return jsonify(robots_list)


@app.route("/get_geolocation", methods=["GET", "POST"])
def get_geolocation():
    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    with session_scope() as session:
        if latitude is not None and longitude is not None:
            update_user_location(session, longitude, latitude, current_user)
        elif latitude is None and longitude is None:
            update_user_location_domicile(session, current_user)
        user = get_user(session, current_user.username)
        print(user)
    return jsonify({"redirect": url_for("user_homepage")})
