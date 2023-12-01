from app.models import Base
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(40), nullable=False, unique=True)
    hashed_password = Column(String(240), nullable=False)
    disabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"UserRobot('{self.id}', '{self.username}', '{self.hashed_password}', '{self.disabled}')"