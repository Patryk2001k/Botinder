from datetime import datetime

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models import Base


class UserMessage(Base):
    __tablename__ = "user_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(550), nullable=False)
    chatroom_id = Column(Integer, ForeignKey("chatrooms.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    message_sender = Column(
        Enum("user", "robot", name="Message_Sender"), nullable=False
    )

    chatrooms = relationship("ChatRoom", back_populates="user_messages")

    def __repr__(self):
        return (
            f"UserMessages('{self.message}', '{self.timestamp}', '{self.chatroom_id}')"
        )
