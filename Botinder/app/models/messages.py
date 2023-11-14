from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class ChatRoom(Base):
    __tablename__ = "chatrooms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    robot_id = Column(Integer, ForeignKey("user_robot.id"), nullable=False)

    user = relationship("User", back_populates="chatrooms")
    robot = relationship("UserRobot", back_populates="chatrooms")
    user_messages = relationship("UserMessages", back_populates="chatroom")

    def __repr__(self):
        return (
            f"ChatRoom('{self.id}', UserId'{self.user_id}', RobotId'{self.robot_id}')"
        )


class UserMessages(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(550), nullable=False)
    chatroom_id = Column(Integer, ForeignKey("chatrooms.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_sender = Column(
        Enum("user", "robot", name="Message_Sender"), nullable=False
    )

    chatroom = relationship("ChatRoom", back_populates="user_messages")

    def __repr__(self):
        return (
            f"UserMessages('{self.message}', '{self.timestamp}', '{self.chatroom_id}')"
        )
