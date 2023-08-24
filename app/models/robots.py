from app.models import *


class UserRobot(Base):
    __tablename__ = "user_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    image_file = Column(String(40), nullable=False, default="default.jpg")
    location = Column(Geography(geometry_type="POINT", srid=4326))
    domicile_geolocation = Column(Geography(geometry_type="POINT", srid=4326))
    messages = relationship("RobotMessages", backref="author", lazy=True)
    profile_robot = relationship(
        "RobotProfile", uselist=False, back_populates="user_robot"
    )

    def __repr__(self):
        return f"UserRobot('{self.name}', '{self.image_file}')"


class RobotMessages(Base):
    __tablename__ = "messages_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)

    def __repr__(self):
        return f"RobotMessages('{self.message}')"


class RobotProfile(Base):
    __tablename__ = "profile_robot"

    id = Column(Integer, primary_key=True, autoincrement=True)
    type_of_robot = Column(
        Enum("humanoid", "non-humanoid", name="Type_of_robot_RobotProfile"),
        nullable=False,
    )
    name = Column(String(20), nullable=False)
    profile_description = Column(String(500), nullable=False)
    domicile = Column(String(80), nullable=False)
    procesor_unit = Column(String(120), nullable=False)
    employment_status = Column(
        Enum("working robot", "disabled", name="Employment_status_RobotProfile"),
        nullable=False,
    )

    user_id = Column(Integer, ForeignKey("user_robot.id"), unique=True)
    user_robot = relationship("UserRobot", back_populates="profile_robot")

    def __repr__(self):
        return f"RobotProfile('{self.user_robot}', '{self.type_of_robot}', '{self.name}', '{self.profile_description}', '{self.domicile}', '{self.procesor_unit}', '{self.employment_status}')"
