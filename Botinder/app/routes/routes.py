from random import randint
from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

# Definicja Bluepinta dla głównych tras aplikacji
main_bp = Blueprint('main', __name__)

@main_bp.route("/")
@main_bp.route("/home")
def home():
    # Zapisujemy adres IP w konfiguracji Flaska
    from flask import current_app
    current_app.config['STATIC_USER_IP'] = request.remote_addr
    
    if current_user.is_authenticated:
        return redirect(url_for("main.user_homepage")) # Zwróć uwagę na przedrostek blueprinta: 'main.'
    else:
        return render_template("main/start-page.html")


@main_bp.route("/lore")
def lore():
    return render_template("main/lore.html")


@main_bp.route("/FAQ")
def FAQ():
    return render_template("main/FAQ.html")


@main_bp.route("/user_homepage", methods=["GET"])
@login_required
def user_homepage():
    from app.services.database_operations.database_operations import (
        get_matched_robots, session_scope)
    from app.services.helpers import generate_robots, robot_to_dict
    from app.services.robot_match.robot_selector import get_robots_for_user

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


@main_bp.route("/unmatch", methods=["POST"])
@login_required
def unmatch():
    from app.models.matches import UnMatches
    from app.services.database_operations.database_operations import (
        add_match_unmatch, session_scope)

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


@main_bp.route("/match", methods=["POST"])
@login_required
def match():
    from app.models.matches import RobotMatches, UserMatches
    from app.services.database_operations.database_operations import (
        add_chatroom, add_match_unmatch, get_robot_info_by_chatroom_id,
        get_single_matched_robot, session_scope)

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


@main_bp.route("/chatroom/<chatroom_id>")
@login_required
def chatroom(chatroom_id):
    from app.services.database_operations.database_operations import (
        get_chatroom_messages, get_matched_robots,
        get_robot_info_by_chatroom_id, session_scope)

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


@main_bp.route("/chatroom_unmatch", methods=["POST"])
@login_required
def chatroom_unmatch():
    from app.models.matches import UnMatches
    from app.services.database_operations.database_operations import (
        add_match_unmatch, delete_chatroom, delete_matched_pair, session_scope)

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
            UnMatches,
        )
        delete_chatroom(session, chatroom_id)
        delete_matched_pair(session, user_name, robot_name)
    return jsonify({"status": "success"})


@main_bp.route("/send_message", methods=["POST"])
def send_message():
    from app.services.database_operations.database_operations import (
        add_message_to_chatroom, session_scope)
    from app.services.tasks.tasks import calL_GPT_API

    try:
        client_data = request.json
        GPT_response = calL_GPT_API()

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


@main_bp.route("/get_robots", methods=["GET", "POST"])
@login_required
def get_robots():
    from app.services.database_operations.database_operations import session_scope
    from app.services.helpers import robot_to_dict
    from app.services.robot_match.robot_selector import get_robots_for_user

    with session_scope() as session:
        robots_list = robot_to_dict(get_robots_for_user(current_user, session))
        return jsonify(robots_list)


@main_bp.route("/get_geolocation", methods=["GET", "POST"])
def get_geolocation():
    from app.services.database_operations.database_operations import (
        get_user, session_scope, update_user_location,
        update_user_location_domicile)

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
    return jsonify({"redirect": url_for("main.user_homepage")})