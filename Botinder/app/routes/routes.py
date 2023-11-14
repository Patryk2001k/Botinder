from random import randint

from flask import jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import app, socketio
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
    get_not_matched_robots_by_localization,
    session_scope,
    get_single_matched_robot
)
from app.services.database_operations.robots_generator.generate_robots import (
    generate_random_robots,
)
from app.services.geolocalization_services.user_localization_and_distance import (
    get_coordinates,
)
from app.services.helper_functions import generate_robots, robot_to_dict
from app.services.image_upload import get_image
from app.services.robot_match.robot_selector import get_robots_for_user
from app.services.tasks.tasks import enqueue_GPT_call

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
    with session_scope() as session:
        robots_list = get_robots_for_user(current_user, session)
        print(robots_list)
        if not robots_list:
            print("?")
            print(get_not_matched_robots_by_localization(current_user, session))
            generate_robots(current_user=current_user, session=session, number_of_robots=5000)
            robots_list = get_robots_for_user(current_user, session)
            print(robots_list)
        matched_robots = get_matched_robots(
            session, current_user.id, current_user.name, include_chatroom_id="yes"
        )
        #print(matched_robots)
        #print("-----------------------")
        #print(matched_robots[0])
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
            session, current_user.id, current_user.name, data["id"], data["name"], UnMatches
        )

    return jsonify({"message": "Successfully matched"}), 200


@app.route("/match", methods=["POST"])
@login_required
def match():
    data = request.get_json()
    with session_scope() as session:
        add_match_unmatch(
            session, current_user.id, current_user.name, data["id"], data["name"], UserMatches
        )

        random_match = randint(0, 2)
        if random_match == 1:
            
            
                add_match_unmatch(
                session, current_user.id, current_user.name, data["id"], data["name"], RobotMatches
                )
                add_chatroom(session, current_user.id, data["id"])
                match_result = get_single_matched_robot(current_user.id, current_user.name, data["id"], session)
                robot_info = get_robot_info_by_chatroom_id(session, match_result[1])
                print("TUTAJ")
                print(match_result)
                print(robot_info)
                match_result_json = {
                    "robot_image": robot_info.image_file,
                    "chatroom_id": match_result[1],
                    "robot_name": robot_info.name
                }

                return jsonify({"message": "Succes", "match_result": match_result_json}), 200

    return jsonify({"message": "No match"}), 400

@app.route("/chatroom/<chatroom_id>")
@login_required
def chatroom(chatroom_id):
    with session_scope() as session:
        matched_robots = get_matched_robots(
             session, current_user.id, current_user.name, include_chatroom_id="yes"
        )
        robot_info = get_robot_info_by_chatroom_id(session, chatroom_id)
        chat_messages = get_chatroom_messages(session, chatroom_id)
        print(chat_messages)
        return render_template(
            "user_homepage/chatroom.html",
            chatroom_id=chatroom_id,
            matched_robots=matched_robots,
            robot_info=robot_info,
            messages=chat_messages,
        )


@socketio.on('message_from_client')
def process_client_message(client_data):
    try:
        
        print('received message: ' + client_data['message'])
        queued_data = [["new", client_data["message"]]]
        queued_task = enqueue_GPT_call.schedule((queued_data), delay=1)
        
        try:
            queued_task_block = queued_task(blocking=True, timeout=10)  # Timeout po 10 sekundach
        except TimeoutError:
            print("Task timed out.")
            return
        
        with session_scope() as session:
            add_message_to_chatroom(session, client_data["message"], client_data["chatroom_id"])
            add_message_to_chatroom(session, queued_task_block, client_data["chatroom_id"], "robot")
        print("QUEUED_TASK_BLOCK")
        print(queued_task_block)
        try:
            socketio.emit('message_from_server', {'message': queued_task_block})
        except ConnectionError:
            print("Could not send message to client, client disconnected.")
    except Exception as e:
        print(f"An error occurred: {e}")

@app.route("/get_robots", methods=["GET", "POST"])
@login_required
def get_robots():
    with session_scope() as session:
        robots_list = robot_to_dict(get_robots_for_user(current_user, session))
        return jsonify(robots_list)


@app.route("/get_geolocation", methods=["GET", "POST"])
def get_geolocation():
    data = request.get_json()
    print(current_user.username)

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    print(f"{latitude}, {longitude}")
    with session_scope() as session:
        update_user_location(session, longitude, latitude, current_user)
        user = get_user(session, current_user.username)
        print(user)
    return jsonify({"redirect": url_for("user_homepage")})


@app.route("/admin_site", methods=["GET", "POST"])
@login_required
def admin_site():
    form = AdminForm()
    if form.validate_on_submit():
        image_name = get_image(form.photo.data, form.name.data, "robots")
        with session_scope() as session:
            insert_into_robots_db(
                session,
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
