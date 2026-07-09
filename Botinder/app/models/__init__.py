from datetime import datetime
from os import environ

from flask_login import LoginManager, UserMixin
from geoalchemy2 import Geography
from sqlalchemy import (Boolean, Column, Enum, ForeignKey, Integer, MetaData,
                        String, create_engine, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session # POPRAWKA: Import scoped_session
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
metadata = MetaData()
DB_URL = DATABASE_URL = environ.get(
    "DATABASE_URL", 
    "postgresql://stary_uzytkownik:stare_haslo@localhost:5432/stara_baza"
)
engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    print("DB was created.")
with engine.connect() as connection:
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
    connection.commit()

from app.models.chatroom import ChatRoom
from app.models.matches import MatchBase, RobotMatches, UnMatches, UserMatches
from app.models.messages import UserMessage
from app.models.robots import *
from app.models.user import *

Base.metadata.create_all(bind=engine)

# POPRAWKA: Tworzymy fabrykę sesji i powiązujemy ją z mechanizmem scoped_session
Session = sessionmaker(bind=engine)
session = scoped_session(Session) # Gwarantuje bezpieczeństwo wątkowe (Thread-safety)