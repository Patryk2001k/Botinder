from datetime import datetime

from flask_login import LoginManager, UserMixin
from geoalchemy2 import Geography
from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    String,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
metadata = MetaData()
DB_URL = "postgresql://postgres:admin@localhost/botinder"

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("Utworzono bazę danych.")

from app.models import Matches
from app.models.messages import Messages
from app.models.robots import RobotMessages, RobotProfile, UserRobot
from app.models.user import Profile, User, UserCriteria

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
session.close()
