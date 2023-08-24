from app.models import *


class Matches(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user_username = Column(String(20), nullable=True)
    robot_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)
    robot_name = Column(String(20), nullable=True)
    # timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="matches")
    robot = relationship("UserRobot", backref="matches")

    def __repr__(self):
        return f"Match('{self.user_id}', '{self.robot_id}')"
