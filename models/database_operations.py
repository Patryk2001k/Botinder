from models import database
from app import bcrypt
from models.database import User, sessionmaker, engine, UserCriteria
Session = sessionmaker(bind=engine)

def user_in_database(name, password):
    session = Session()
    #user_exists = session.query(database.exists().where(database.User.name == name)).scalar()
    user_password = session.query(database.User.password).filter_by(name=name).first()
    check_password = ""
    
    if user_password is not None:
        check_password = bcrypt.check_password_hash(user_password[0], password)

    session.close()

    if check_password:
        return True
    else:
        return False


def insert_user_and_user_profile(name, lastname, password, email, age, gender, profile_description, domicile, education, 
                                 employment_status, type_of_robot, distance, employment_status_criteria):
        session = Session()
        
        hashed_password = bcrypt.generate_password_hash(password)
        user = database.User(name=name, email=email, lastname=lastname, password=hashed_password)
        session.add(user)
        session.commit()

        profile = database.Profile(
            age=age,
            gender=gender,
            profile_description=profile_description,
            domicile=domicile,
            education=education,
            employment_status=employment_status,
            user=user
        )

        criteria = UserCriteria(
             type_of_robot=type_of_robot,
             distance=distance,
             employment_status=employment_status_criteria,
             user=user
        )

        session.add(profile)
        session.add(criteria)
        session.commit()

        session.close()

def insert_into_user_criteria_db():
     return 

def insert_into_robots_db(name, type_of_robot, profile_description, domicile, procesor_unit, employment_status):
        session_1 = Session()
        
        user_robot = database.UserRobot(name=name)
        session_1.add(user_robot)
        session_1.commit()

        robot_profile = database.RobotProfile(
            type_of_robot=type_of_robot,
            name=name,
            profile_description=profile_description,
            domicile=domicile,
            procesor_unit=procesor_unit,
            employment_status=employment_status,
            user_robot=user_robot
        )
        session_1.add(robot_profile)
        session_1.commit() 
        session_1.close()

def select_all_from_database(model_class):
     session_2 = Session()
     all_information_from_db = session_2.query(model_class).all()
     session_2.close()
     return all_information_from_db

def get_user_from_User_table(user):
     session_3 = Session()
     selected_user = session_3.query(User).filter_by(name=user).first()
     session_3.close()
     return selected_user

