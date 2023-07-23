from datetime import datetime

from flask_login import LoginManager, UserMixin
from sqlalchemy import (Column, Enum, ForeignKey, Integer, String,
                        create_engine, MetaData, Text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from geoalchemy2 import Geography

Base = declarative_base()
metadata = MetaData()
DB_URL = "postgresql://postgres:admin@localhost/botinder"

from app import app

login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).get(int(user_id))


class User(Base, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    lastname = Column(String(40), nullable=False)
    email = Column(String(120), nullable=False)
    image_file = Column(String(240), nullable=False, default="default.jpg")
    password = Column(Text, nullable=False)
    #location = Column(Geography(geometry_type='POINT', srid=4326))
    #domicile_geolocation = Column(Geography(geometry_type='POINT', srid=4326))
    messages = relationship("Messages", backref="author", lazy=True)
    profile = relationship("Profile", uselist=False, back_populates="user")
    user_criteria = relationship("UserCriteria", uselist=False, back_populates="user")

    def __repr__(self):
        return f"User('{self.name}', '{self.lastname}','{self.email}', '{self.password}', '{self.image_file}', '{self.location}')"


class Messages(Base, UserMixin):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Messages('{self.name}', {self.email}, '{self.message}')"


class Profile(Base, UserMixin):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(Enum("male", "female", "custom", name="Gender_Profile"), nullable=False)
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    education = Column(String(120), nullable=False)
    employment_status = Column(Enum("hired", "unemployed", "student", name="Employment_status_Profile"), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.age}', '{self.gender}', '{self.profile_description}', '{self.domicile}', '{self.education}', '{self.employment_status}')"


class UserCriteria(Base, UserMixin):
    __tablename__ = "user_criteria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(Enum("humanoid", "non-humanoid", "all", name="Type_of_robot_UserCriteria"), nullable=False)
    distance = Column(Integer, nullable=False)
    employment_status = Column(Enum("working robot", "disabled", "all", name="Employment_status_UserCriteria"), nullable=False)

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="user_criteria")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.type_of_robot}', '{self.distance}', '{self.employment_status}')"


# Poniższe bazy danych dotyczą robotów (NPC) na stronie


class UserRobot(Base, UserMixin):
    __tablename__ = "user_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    image_file = Column(String(40), nullable=False, default="default.jpg")
    #location = Column(Geography(geometry_type='POINT', srid=4326))
    #domicile_geolocation = Column(Geography(geometry_type='POINT', srid=4326))
    messages = relationship("RobotMessages", backref="author", lazy=True)
    profile_robot = relationship(
        "RobotProfile", uselist=False, back_populates="user_robot"
    )

    def __repr__(self):
        return f"UserRobot('{self.name}', '{self.image_file}')"


class RobotMessages(Base, UserMixin):
    __tablename__ = "messages_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)

    def __repr__(self):
        return f"RobotMessages('{self.message}')"


class RobotProfile(Base, UserMixin):
    __tablename__ = "profile_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(Enum("humanoid", "non-humanoid", "all", name="Type_of_robot_RobotProfile"), nullable=False)
    name = Column(String(20), nullable=False)
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    procesor_unit = Column(String(120), nullable=False)
    employment_status = Column(Enum("working robot", "disabled", "all", name="Employment_status_RobotProfile"), nullable=False)

    user_id = Column(Integer, ForeignKey("user_robot.id"), unique=True)
    user_robot = relationship("UserRobot", back_populates="profile_robot")

    def __repr__(self):
        return f"RobotProfile('{self.user_robot}', '{self.type_of_robot}', '{self.name}', '{self.profile_description}', '{self.domicile}', '{self.procesor_unit}', '{self.employment_status}')"

# Poniżej znajduje się baza danych dla admina


class Admins(Base, UserMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)
    #location = Column(Geography(geometry_type='POINT', srid=4326))

    def __repr__(self):
        return f"Admins({self.name}, {self.password})"
    
    

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("Utworzono bazę danych.")

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()
