from datetime import datetime

from flask_login import LoginManager, UserMixin
from geoalchemy2 import Geography
from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer, MetaData,
                        String, create_engine, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import create_database, database_exists

# from sqlalchemy.dialects.postgresql import UUID #UUID for the future
# import uuid

Base = declarative_base()
metadata = MetaData()
DB_URL = "" #Put your DB URL here
engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("DB was created.")
with engine.connect() as connection:
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))


from app.models.chatroom import ChatRoom
from app.models.matches import MatchBase, RobotMatches, UnMatches, UserMatches
from app.models.messages import UserMessage
from app.models.robots import *
from app.models.user import *

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
