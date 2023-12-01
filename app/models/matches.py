from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class MatchBase(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_username = Column(String(20), nullable=True)
    robot_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)
    robot_name = Column(String(20), nullable=True)
    match_type = Column(String(50))
    # timestamp = Column(DateTime, default=datetime.utcnow)

    __mapper_args__ = {"polymorphic_identity": "matches", "polymorphic_on": match_type}

    def __repr__(self):
        return f"Match('{self.user_id}', '{self.robot_id}', '{self.user_username}', '{self.robot_name}')"


class UserMatches(MatchBase):
    __mapper_args__ = {
        "polymorphic_identity": "user_matches",
    }

    user = relationship("User", back_populates="user_matches_1")
    robot = relationship("UserRobot", back_populates="robot_matches_1")

    def __repr__(self):
        return f"UserMatch('{self.user_id}', '{self.robot_id}', '{self.user_username}', '{self.robot_name}')"


class RobotMatches(MatchBase):
    __mapper_args__ = {
        "polymorphic_identity": "robot_matches",
    }

    user = relationship("User", back_populates="user_matches")
    robot = relationship("UserRobot", back_populates="robot_matches")

    def __repr__(self):
        return f"RobotMatch('{self.user_id}', '{self.robot_id}', '{self.user_username}', '{self.robot_name}')"


class UnMatches(MatchBase):
    __mapper_args__ = {
        "polymorphic_identity": "unmatches",
    }
    # user = relationship("User", backref="unmatches")
    # robot = relationship("UserRobot", backref="unmatches")

    def __repr__(self):
        return f"UnMatch('{self.user_id}', '{self.robot_id}', '{self.user_username}', '{self.robot_name}')"
