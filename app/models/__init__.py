from datetime import datetime

from flask_login import LoginManager, UserMixin
from sqlalchemy import (Column, Enum, ForeignKey, Integer, String,
                        create_engine, MetaData)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import database_exists, create_database
from geoalchemy2 import Geography

Base = declarative_base()
metadata = MetaData()
DB_URL = "postgresql://postgres:admin@localhost/botinder"

"""

"""

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("Utworzono bazę danych.")

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()

from app.models.admin import Admins
from app.models.user import User, Profile, UserCriteria
from app.models.robots import RobotMessages, RobotProfile, UserRobot
from app.models.messages import Messages

