from contextlib import contextmanager

from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import to_shape
from sqlalchemy import and_, asc, exists, not_, or_
from sqlalchemy.orm import aliased, joinedload, sessionmaker

from app import bcrypt
from app.models import Session, engine, session
from app.models.chatroom import ChatRoom
from app.models.matches import MatchBase, RobotMatches, UserMatches
from app.models.messages import UserMessage
from app.models.robots import RobotProfile, UserRobot
from app.models.user import Profile, User, UserCriteria
from app.services.geolocalization_services.user_localization_and_distance import \
    get_coordinates


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


class UserObject:
    def __init__(self, name):
        self.name = name
        self.user = session.query(User).filter_by(name=name).first()
        session.close()

    def user_exists(self):
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
    session,
):
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(
        username=username,
        name=name,
        email=email,
        image_file=image_file,
        lastname=lastname,
        password=hashed_password,
        #domicile_geolocation=domicile_location,
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
    session,
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

def update_user_location_domicile(session, user):
    user.location = user.domicile_geolocation
    user.domicile_geolocation = user.domicile_geolocation
    session.commit()

def update_user_location(session, longitude, latitude, user):
    new_user_location = WKTElement(f"POINT({longitude} {latitude})", srid=4326)

    user.location = new_user_location

    session.commit()


def select_all_from_database(model_class):
    return session.query(model_class).all()


def get_user(session, name):
    return session.query(User).filter_by(name=name).first()


def get_not_matched_robots_by_localization(user, session):
    distance = user.user_criteria.distance * 1000  # distance * 1000 this value is in km
    MAX_ROBOTS = 100
    if user.location:
        current_user_location = user.location
    else:
        current_user_location = to_shape(user.domicile_geolocation).wkt

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
            ST_DWithin(UserRobot.location, current_user_location, distance),
        )
        .limit(MAX_ROBOTS)
        .all()
    )  # Set robots limit

    return robots_within_distance_not_matched


def get_user_criteria(user, session):
    user_criteria = (
        session.query(UserCriteria).filter(UserCriteria.user_id == user.id).first()
    )
    return user_criteria


def add_match_unmatch(session, user_id, user_name, robot_id, robot_name, table_model):
    new_match = table_model(
        user_id=user_id,
        user_name=user_name,
        robot_id=robot_id,
        robot_name=robot_name,
    )
    session.add(new_match)
    session.commit()


def get_user_matches(session, user_id, user_name):
    return (
        session.query(UserMatches).filter_by(user_id=user_id, user_name=user_name).all()
    )


def get_robot_matches(session, user_id, user_name):
    return (
        session.query(RobotMatches)
        .filter_by(user_id=user_id, user_name=user_name)
        .all()
    )


def find_common_matches(user_matches, robot_matches):
    user_match_ids = [match.robot_id for match in user_matches]
    robot_match_ids = [match.robot_id for match in robot_matches]
    return list(set(user_match_ids) & set(robot_match_ids))


def include_chatroomid(session, user_id, common_matched_robot_ids):
    chatroom_query = (
        session.query(ChatRoom)
        .filter(
            ChatRoom.user_id == user_id,
            ChatRoom.robot_id.in_(common_matched_robot_ids),
        )
        .all()
    )
    return {chatroom.robot_id: chatroom.id for chatroom in chatroom_query}


def get_matched_robots(session, user_id, user_name, include_chatroom_id=False):
    user_matches = get_user_matches(session, user_id, user_name)
    robot_matches = get_robot_matches(session, user_id, user_name)

    common_matched_robot_ids = find_common_matches(user_matches, robot_matches)

    if include_chatroom_id:
        chatroom_ids = include_chatroomid(session, user_id, common_matched_robot_ids)
        matched_with_chatroom = []
        for match in user_matches:
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
            UserMatches.user_name == user_name,
            RobotMatches_query,
        )

        return UserRobot_query.all()


def get_single_matched_robot(user_id, user_name, robot_id, session):
    # Find single matched user from UserMatches
    user_match = (
        session.query(UserMatches)
        .filter_by(user_id=user_id, user_name=user_name, robot_id=robot_id)
        .first()
    )

    # If no match found in UserMatches, return None
    if not user_match:
        return None

    # Check if this robot is also matched in RobotMatches
    robot_match = (
        session.query(RobotMatches)
        .filter_by(user_id=user_id, user_name=user_name, robot_id=robot_id)
        .first()
    )

    # If the robot is not mutually matched, return None
    if not robot_match:
        return None

    # Query for the chatroom ID
    chatroom = (
        session.query(ChatRoom).filter_by(user_id=user_id, robot_id=robot_id).first()
    )

    # Return the user match along with the chatroom ID, if it exists
    if chatroom:
        return user_match, chatroom.id
    else:
        return user_match, None


def add_chatroom(session, user_id, robot_id):
    chatroom = ChatRoom(user_id=user_id, robot_id=robot_id)
    session.add(chatroom)
    session.commit()


def get_robot_info_by_chatroom_id(session, chatroom_id):
    chatroom = session.query(ChatRoom).filter_by(id=chatroom_id).first()
    if chatroom is not None:
        robot = chatroom.robot
        return robot
    else:
        return None


def get_chatroom_messages(session, chatroom_id):
    messages_query = (
        session.query(UserMessage)
        .filter_by(chatroom_id=chatroom_id)
        .order_by(asc(UserMessage.timestamp))
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


def add_message_to_chatroom(session, message, chatroom_id, message_sender="user"):
    new_message = UserMessage(
        message=message, chatroom_id=chatroom_id, message_sender=message_sender
    )
    session.add(new_message)
    session.commit()


def delete_chatroom(session, chatroom_id):
    session.query(UserMessage).filter(UserMessage.chatroom_id == chatroom_id).delete()
    chatroom_to_delete = (
        session.query(ChatRoom).filter(ChatRoom.id == chatroom_id).one_or_none()
    )
    if chatroom_to_delete:
        session.delete(chatroom_to_delete)
        session.commit()
        print(f"Chatroom with ID {chatroom_id} has been deleted.")
    else:
        print(f"Chatroom with ID {chatroom_id} not found.")


def delete_matched_pair(session, user_name, robot_name):
    user = session.query(User).filter(User.name == user_name).first()
    robot = session.query(UserRobot).filter(UserRobot.name == robot_name).first()

    if not user or not robot:
        return

    user_match = (
        session.query(UserMatches)
        .filter(UserMatches.user_id == user.id, UserMatches.robot_id == robot.id)
        .first()
    )

    robot_match = (
        session.query(RobotMatches)
        .filter(RobotMatches.user_id == user.id, RobotMatches.robot_id == robot.id)
        .first()
    )

    if user_match and robot_match:
        session.delete(user_match)
        session.delete(robot_match)
        session.commit()
    else:
        print(
            f"Match not found in both UserMatches and RobotMatches for User '{user_name}' and Robot '{robot_name}'."
        )
