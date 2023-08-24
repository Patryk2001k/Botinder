from app.models import *


class Messages(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    message = Column(String(400), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Messages('{self.name}', {self.email}, '{self.message}')"
