from app.models import *

class Admins(Base, UserMixin):
    __tablename__ = "admins"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    password = Column(String(120), nullable=False)
    location = Column(Geography(geometry_type='POINT', srid=4326))

    def __repr__(self):
        return f"Admins({self.name}, {self.password})"
    