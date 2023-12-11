from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models import Base


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    robot_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)

    user = relationship("User", back_populates="chatrooms")
    robot = relationship("UserRobot", back_populates="chatrooms")
    user_messages = relationship("UserMessage", back_populates="chatrooms")

    def __repr__(self):
        return (
            f"ChatRoom('{self.id}', UserId'{self.user_id}', RobotId'{self.robot_id}')"
        )
