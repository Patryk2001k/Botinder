from flask import Blueprint, jsonify, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required

# Wszystkie importy przeniesione na samą górę pliku
from app.services.matchmaking import MatchmakingService
from app.services.chat import ChatService
from app.services.database_operations import (
    get_user, session_scope, update_user_location, update_user_location_domicile
)

main_bp = Blueprint('main', __name__)


@main_bp.route("/")
@main_bp.route("/home")
def home():
    current_app.config['STATIC_USER_IP'] = request.remote_addr
    
    if current_user.is_authenticated:
        return redirect(url_for("main.user_homepage"))
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
    robots_list = MatchmakingService.get_candidate_robots(current_user)
    matched_robots = MatchmakingService.get_matches(current_user)
    
    return render_template(
        "user_homepage/user_homepage.html",
        user=current_user.username,
        robots_list=robots_list,
        matched_robots=matched_robots,
    )


@main_bp.route("/unmatch", methods=["POST"])
@login_required
def unmatch():
    data = request.get_json()
    MatchmakingService.unmatch_robot(
        user=current_user, 
        robot_id=data["id"], 
        robot_name=data["name"]
    )
    return jsonify({"message": "Successfully unmatched"}), 200


@main_bp.route("/match", methods=["POST"])
@login_required
def match():
    data = request.get_json()
    match_result = MatchmakingService.match_robot(
        user=current_user,
        robot_id=data["id"],
        robot_name=data["name"]
    )
    
    if match_result:
        return jsonify({"message": "Success", "match_result": match_result}), 200
    return jsonify({"message": "No match"}), 200


@main_bp.route("/chatroom/<chatroom_id>")
@login_required
def chatroom(chatroom_id):
    chat_context = ChatService.get_chatroom_context(current_user, int(chatroom_id))
    
    return render_template(
        "user_homepage/chatroom.html",
        chatroom_id=chatroom_id,
        user=current_user.username,
        matched_robots=chat_context["matched_robots"],
        robot_info=chat_context["robot_info"],
        messages=chat_context["messages"],
    )


@main_bp.route("/chatroom_unmatch", methods=["POST"])
@login_required
def chatroom_unmatch():
    data = request.get_json()
    ChatService.unmatch_chatroom(
        user=current_user,
        chatroom_id=int(data.get("chatroomId")),
        robot_id=int(data.get("robotId")),
        robot_name=data.get("robotName"),
        user_name=data.get("userName")
    )
    return jsonify({"status": "success"})


@main_bp.route("/send_message", methods=["POST"])
def send_message():
    try:
        client_data = request.json
        gpt_response = ChatService.process_user_message(
            chatroom_id=int(client_data["chatroom_id"]),
            message_text=client_data["message"]
        )
        return jsonify({"message": gpt_response})
    except Exception as e:
        print(f"Błąd krytyczny w send_message: {e}")
        return jsonify({"error": str(e)}), 500


@main_bp.route("/get_robots", methods=["GET", "POST"])
@login_required
def get_robots():
    robots_list = MatchmakingService.get_candidate_robots(current_user)
    return jsonify(robots_list)


@main_bp.route("/get_geolocation", methods=["GET", "POST"])
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
    return jsonify({"redirect": url_for("main.user_homepage")})