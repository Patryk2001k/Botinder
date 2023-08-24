from geoalchemy2.elements import WKTElement
from geoalchemy2.functions import ST_DWithin
from sqlalchemy import and_, exists, not_
from sqlalchemy.orm import joinedload

from app import bcrypt
from app.models import (
    Matches,
    Profile,
    RobotProfile,
    User,
    UserCriteria,
    UserRobot,
    engine,
    sessionmaker,
)
from app.services.geolocalization_services.user_localization_and_distance import (
    get_coordinates,
)

Session = sessionmaker(bind=engine)
session = Session()


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
    distance = 50 * 1000  # 50 km przeliczone z metrów
    MAX_ROBOTS = 50

    robots_within_distance_not_matched = (
        session.query(UserRobot)
        .options(
            joinedload(UserRobot.profile_robot)  # Dołączamy profile w jednym zapytaniu
        )
        .filter(
            # Filtrowanie robotów, którzy nie są w tabeli Matches dla danego użytkownika
            not_(
                UserRobot.id.in_(
                    session.query(Matches.robot_id).filter(Matches.user_id == user.id)
                )
            ),
            # Filtrowanie robotów w określonej odległości od punktu odniesienia
            ST_DWithin(UserRobot.location, user.location, distance),
        )
        .limit(MAX_ROBOTS)
        .all()
    )  # Ustawienie limitu robotów

    return robots_within_distance_not_matched


def add_match(user_id, robot_id):
    new_match = Matches(user_id=user_id, robot_id=robot_id)
    session.add(new_match)
    session.commit()
    return


def get_user_criteria(user):
    user_criteria = (
        session.query(UserCriteria).filter(UserCriteria.user_id == user.id).first()
    )
    return user_criteria


def download_matched_users(user, reference_point):
    pass
