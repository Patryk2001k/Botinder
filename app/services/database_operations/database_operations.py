from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
from sqlalchemy import and_, asc, exists, not_, or_
from sqlalchemy.orm import aliased, joinedload

from app import bcrypt
from app.models import engine, session
from app.models.matches import RobotMatches, UserMatches
from app.models.messages import ChatRoom, UserMessages
from app.models.robots import RobotProfile, UserRobot
from app.models.user import Profile, User, UserCriteria
from app.services.geolocalization_services.user_localization_and_distance import (
    get_coordinates,
)


class UserObject:
    def __init__(self, username):
        self.username = username
        self.user = session.query(User).filter_by(username=username).first()
        session.close()

    def user_exists(self):
        print(self.user)
        return self.user is not None

    def password_exists(self, password):
        users = session.query(User).all()
        password_exists = False
        for user in users:
            if bcrypt.check_password_hash(user.password, password):
                password_exists = True
                break
        session.close()
        return password_exists

    def check_user_in_db_registration(self, password):
        return self.user_exists() or self.password_exists(password)

    def check_user_in_db_login(self, password):
        return self.user_exists() and self.password_exists(password)

    def is_admin(self):
        return self.user_exists() and self.user.is_admin


def insert_user_and_user_profile(
    username,
    name,
    lastname,
    password,
    email,
    image_file,
    age,
    gender,
    profile_description,
    domicile,
    education,
    employment_status_profile,
    type_of_robot,
    distance,
    employment_status_criteria,
):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    domicile_longitude_and_latitude = get_coordinates(domicile)
    longitude = domicile_longitude_and_latitude[0]
    latitude = domicile_longitude_and_latitude[1]
    domicile_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

    user = User(
        username=username,
        name=name,
        email=email,
        image_file=image_file,
        lastname=lastname,
        password=hashed_password,
        domicile_geolocation=domicile_location,
        # is_admin=True
    )

    profile = Profile(
        age=age,
        gender=gender,
        profile_description=profile_description,
        domicile=domicile,
        education=education,
        employment_status=employment_status_profile,
        user=user,
    )

    criteria = UserCriteria(
        type_of_robot=type_of_robot,
        distance=distance,
        employment_status=employment_status_criteria,
        user=user,
    )

    session.add(user)
    session.add(profile)
    session.add(criteria)
    session.commit()


def insert_into_robots_db(
    name,
    image_file,
    type_of_robot,
    profile_description,
    domicile,
    procesor_unit,
    employment_status,
):
    user_robot = UserRobot(name=name, image_file=image_file)

    robot_profile = RobotProfile(
        type_of_robot=type_of_robot,
        name=name,
        profile_description=profile_description,
        domicile=domicile,
        procesor_unit=procesor_unit,
        employment_status=employment_status,
        user_robot=user_robot,
    )

    session.add(user_robot)
    session.add(robot_profile)
    session.commit()


def update_user_location(longitude, latitude, user):
    new_user_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

    user.location = new_user_location

    session.commit()


def select_all_from_database(model_class):
    return session.query(model_class).all()


def get_user(user):
    return session.query(User).filter_by(username=user).first()


def get_not_matched_robots_by_localization(user):
    distance = user.user_criteria.distance * 1000  # distance * 1000 this value is in km
    MAX_ROBOTS = 100

    robots_within_distance_not_matched = (
        session.query(UserRobot)
        .options(joinedload(UserRobot.profile_robot))
        .filter(
            # Filter robots that are not in UserMatches table
            not_(
                UserRobot.id.in_(
                    session.query(UserMatches.robot_id).filter(
                        UserMatches.user_id == user.id
                    )
                )
            ),
            # Filter by localization
            ST_DWithin(UserRobot.location, user.location, distance),
        )
        .limit(MAX_ROBOTS)
        .all()
    )  # Set robots limit

    return robots_within_distance_not_matched


def get_user_criteria(user):
    user_criteria = (
        session.query(UserCriteria).filter(UserCriteria.user_id == user.id).first()
    )
    return user_criteria


def add_match_unmatch(user_id, user_username, robot_id, robot_name, table_model):
    new_match = table_model(
        user_id=user_id,
        user_username=user_username,
        robot_id=robot_id,
        robot_name=robot_name,
    )
    session.add(new_match)
    session.commit()


def get_matched_robots(user_id, user_username, include_chatroom_id="no"):
    # Get matched users from UserMatches
    user_matches_query = (
        session.query(UserMatches)
        .filter_by(user_id=user_id, user_username=user_username)
        .all()
    )

    matched_robot_ids = [match.robot_id for match in user_matches_query]

    # Download matched robots from RobotsMatches
    robot_matches_query = (
        session.query(RobotMatches)
        .filter_by(user_id=user_id, user_username=user_username)
        .all()
    )

    matched_robot_ids_from_robot_table = [
        match.robot_id for match in robot_matches_query
    ]

    # Finding common matches
    common_matched_robot_ids = list(
        set(matched_robot_ids) & set(matched_robot_ids_from_robot_table)
    )

    # Download chatroom id if it is necessary
    if include_chatroom_id == "yes":
        chatroom_query = (
            session.query(ChatRoom)
            .filter(
                ChatRoom.user_id == user_id,
                ChatRoom.robot_id.in_(common_matched_robot_ids),
            )
            .all()
        )

        chatroom_ids = {chatroom.robot_id: chatroom.id for chatroom in chatroom_query}

        # Join chatroom id-s to result
        matched_with_chatroom = []
        for match in user_matches_query:
            chatroom_id = chatroom_ids.get(match.robot_id)
            if chatroom_id and match.robot_id in common_matched_robot_ids:
                matched_with_chatroom.append((match, chatroom_id))

        return matched_with_chatroom

    else:
        RobotMatches_query = (
            session.query(RobotMatches)
            .filter(
                RobotMatches.user_id == UserMatches.user_id,
                RobotMatches.robot_id == UserMatches.robot_id,
            )
            .exists()
        )

        UserRobot_query = session.query(UserMatches).filter(
            UserMatches.user_id == user_id,
            UserMatches.user_username == user_username,
            RobotMatches_query,
        )

        matched_users = UserRobot_query.all()
        return matched_users


def add_chatroom(user_id, robot_id):
    chatroom = ChatRoom(user_id=user_id, robot_id=robot_id)
    session.add(chatroom)
    session.commit()


def get_robot_info_by_chatroom_id(chatroom_id):
    chatroom = session.query(ChatRoom).filter_by(id=chatroom_id).first()
    if chatroom is not None:
        robot = chatroom.robot
        return robot
    else:
        return None


def get_chatroom_messages(chatroom_id):
    messages_query = (
        session.query(UserMessages)
        .filter_by(chatroom_id=chatroom_id)
        .order_by(asc(UserMessages.timestamp))
        .all()
    )

    messages = []

    for message in messages_query:
        message_details = {
            "message": message.message,
            "timestamp": message.timestamp,
            "chatroom_id": message.chatroom_id,
        }

        messages.append([message_details, message.message_sender])

    return messages


def add_message_to_chatroom(message, chatroom_id, message_sender="user"):
    new_message = UserMessages(
        message=message, chatroom_id=chatroom_id, message_sender=message_sender
    )
    session.add(new_message)
    session.commit()
