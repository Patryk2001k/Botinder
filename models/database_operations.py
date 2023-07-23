from app import bcrypt
from models import database
from models.database import (Admins, RobotProfile, User, UserCriteria,
                             UserRobot, engine, sessionmaker)
from sqlalchemy import exists
Session = sessionmaker(bind=engine)

def user_in_database(password, username):
    session = Session()

    user_exists = session.query(exists().where(User.username == username)).scalar()

    if user_exists:
        user = session.query(User).filter_by(username=username).first()
        if bcrypt.check_password_hash(user.password, password):
            session.close()
            return True
        else:
            return False

    session.close()
    return False



def if_user_is_admin(name, password):
    session = Session()
    user_exists = session.query(
        database.exists().where(database.User.name == name)
    ).scalar()
    print(user_exists)
    admin = session.query(Admins).all()
    is_admin = False

    for x in admin:
        if bcrypt.check_password_hash(x.password, password):
            is_admin = True

    session.close()

    if is_admin and user_exists:
        return True
    else:
        return False


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
    employment_status,
    type_of_robot,
    distance,
    employment_status_criteria,
):
    session = Session()
    hashed_password = bcrypt.generate_password_hash(password)
    print(hashed_password)
    user = database.User(
        username=username,
        name=name,
        email=email,
        image_file=image_file,
        lastname=lastname,
        password=hashed_password,
    )

    profile = database.Profile(
        age=age,
        gender=gender,
        profile_description=profile_description,
        domicile=domicile,
        education=education,
        employment_status=employment_status,
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
    session = Session()
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


def select_all_from_database(model_class):
    session = Session()
    all_information_from_db = session.query(model_class).all()
    return all_information_from_db


def get_user_from_User_table(user):
    session = Session()
    selected_user = session.query(User).filter_by(name=user).first()
    return selected_user
