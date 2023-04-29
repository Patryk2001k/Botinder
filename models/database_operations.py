from models import database
from main_module import bcrypt
from models.database import Session

def user_in_database(username, password):
    user_exists = database.session.query(database.exists().where(database.User.username == username)).scalar()
    user_password = database.session.query(database.User.password).filter_by(username=username).first()
    
    if user_password is not None:
        check_password = bcrypt.check_password_hash(user_password[0], password)

    if user_exists and check_password:
        return True
    else:
        return False


def insert_user_and_user_profile(username, password, email, age, gender, profile_description, domicile, education, employment_status):
        session = Session()
        
        hashed_password = bcrypt.generate_password_hash(password)
        user = database.User(username=username, email=email, password=hashed_password)
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
        session.add(profile)
        session.commit()

def insert_into_user_criteria_db():
     return 

def select_all_from_database(model_class):
     session = Session()
     return session.query(model_class).all()