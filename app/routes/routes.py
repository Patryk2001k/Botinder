from random import randint

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import app
from app.forms.forms import AdminForm
from app.models.matches import RobotMatches, UnMatches, UserMatches
from app.models.robots import RobotProfile, UserRobot
from app.services.database_operations.database_operations import (
    add_chatroom,
    add_match_unmatch,
    add_message_to_chatroom,
    get_chatroom_messages,
    get_matched_robots,
    get_robot_info_by_chatroom_id,
    get_user,
    insert_into_robots_db,
    select_all_from_database,
    update_user_location,
)
from app.services.database_operations.robots_generator.generate_robots import (
    generate_random_robots,
)
from app.services.geolocalization_services.user_localization_and_distance import (
    get_coordinates,
)
from app.services.helper_functions import generate_random_robots, robot_to_dict
from app.services.image_upload import get_image
from app.services.robot_match.robot_selector import get_robots_for_user


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage"))
    else:
        return render_template("main/start-page.html")


@app.route("/lore")
def lore():
    return render_template("main/lore.html")


@app.route("/FAQ")
def FAQ_site():
    return render_template("main/FAQ.html")


@app.route("/user_homepage", methods=["GET"])
@login_required
def user_homepage():
    robots_list = get_robots_for_user(current_user)
    if not robots_list:
        generate_random_robots(current_user, number_of_robots=5000)
        robots_list = get_robots_for_user(current_user)
    matched_robots = get_matched_robots(
        current_user.id, current_user.name, include_chatroom_id="yes"
    )
    return render_template(
        "user_homepage/user_homepage.html",
        user=current_user.name,
        robots_list=robot_to_dict(robots_list),
        matched_robots=matched_robots,
    )


@app.route("/unmatch", methods=["POST"])
@login_required
def unmatch():
    data = request.get_json()

    add_match_unmatch(
        current_user.id, current_user.name, data["id"], data["name"], UnMatches
    )

    return jsonify({"message": "Successfully matched"}), 200


@app.route("/match", methods=["POST"])
@login_required
def match():
    data = request.get_json()

    add_match_unmatch(
        current_user.id, current_user.name, data["id"], data["name"], UserMatches
    )

    random_match = randint(0, 2)
    if random_match == 1:
        add_match_unmatch(
            current_user.id, current_user.name, data["id"], data["name"], RobotMatches
        )
        add_chatroom(current_user.id, data["id"])

    return jsonify({"message": "Successfully matched"}), 200


@app.route("/chatroom/<chatroom_id>")
@login_required
def chatroom(chatroom_id):
    matched_robots = get_matched_robots(
        current_user.id, current_user.name, include_chatroom_id="yes"
    )
    robot_info = get_robot_info_by_chatroom_id(chatroom_id)
    chat_messages = get_chatroom_messages(chatroom_id)
    print(chat_messages)
    return render_template(
        "user_homepage/chatroom.html",
        chatroom_id=chatroom_id,
        matched_robots=matched_robots,
        robot_info=robot_info,
        messages=chat_messages,
    )


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data["message"]
    chatroom_id = data["chatroom_id"]
    add_message_to_chatroom(message, chatroom_id)
    return jsonify({"status": "message sent"}), 200


@app.route("/get_robots", methods=["GET", "POST"])
@login_required
def get_robots():
    robots_list = robot_to_dict(get_robots_for_user(current_user))
    return jsonify(robots_list)


@app.route("/get_geolocation", methods=["GET", "POST"])
def get_geolocation():
    data = request.get_json()
    print(current_user.username)

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    print(f"{latitude}, {longitude}")

    update_user_location(longitude, latitude, current_user)
    user = get_user(current_user.username)
    print(user)
    return jsonify({"redirect": url_for("user_homepage")})


@app.route("/admin_site", methods=["GET", "POST"])
@login_required
def admin_site():
    form = AdminForm()
    if form.validate_on_submit():
        image_name = get_image(form.photo.data, form.name.data, "robots")
        insert_into_robots_db(
            form.name.data,
            image_name,
            form.type_of_robot.data,
            form.profile_description.data,
            form.domicile.data,
            form.procesor_unit.data,
            form.employment_status.data,
        )

        return render_template(
            "auth/admin/admin-site.html",
            form=form,
            message="Udało się dodać użytkownika",
        )
    return render_template("auth/admin/admin-site.html", form=form)
