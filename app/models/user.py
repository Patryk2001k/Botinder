from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base
from app.models.robots import UserRobotBase


class User(UserRobotBase, UserMixin):
    __tablename__ = "user"

    username = Column(String(20), nullable=False)
    lastname = Column(String(40), nullable=False)
    email = Column(String(120), nullable=False)
    password = Column(String(120), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    chatrooms = relationship("ChatRoom", back_populates="user", lazy=True)
    profile = relationship("Profile", uselist=False, back_populates="user")
    user_criteria = relationship("UserCriteria", uselist=False, back_populates="user")
    user_matches = relationship("UserMatches", back_populates="user")
    robot_matches = relationship("RobotMatches", back_populates="user_matches")

    def __repr__(self):
        return f"User('{self.username}', '{self.name}', '{self.lastname}','{self.email}', '{self.password}', '{self.image_file}', '{self.location}', '{self.domicile_geolocation}')"


class Profile(Base):
    __tablename__ = "profile"

    # id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) Z czasem podmienić wszystkie na uuid
    id = Column(Integer, primary_key=True, autoincrement=True)
    age = Column(Integer, nullable=False)
    gender = Column(
        Enum("male", "female", "custom", name="Gender_Profile"), nullable=False
    )
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    education = Column(String(120), nullable=False)
    employment_status = Column(
        Enum("hired", "unemployed", "student", name="Employment_status_Profile"),
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="profile")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.age}', '{self.gender}', '{self.profile_description}', '{self.domicile}', '{self.education}', '{self.employment_status}')"


class UserCriteria(Base):
    __tablename__ = "user_criteria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(
        Enum("humanoid", "non-humanoid", "all", name="Type_of_robot_UserCriteria"),
        nullable=False,
    )
    distance = Column(Integer, nullable=False)
    employment_status = Column(
        Enum("working robot", "disabled", "all", name="Employment_status_UserCriteria"),
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="user_criteria")

    def __repr__(self):
        return f"Profile('{self.user}', '{self.type_of_robot}', '{self.distance}', '{self.employment_status}')"
