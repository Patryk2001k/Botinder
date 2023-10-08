from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

# from sqlalchemy.dialects.postgresql import UUID #UUID for the future
# import uuid

Base = declarative_base()
metadata = MetaData()
DB_URL = "postgresql://postgres:admin@localhost/botinder"
engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
    print("Utworzono bazę danych.")


from app.models.matches import MatchBase, RobotMatches, UnMatches, UserMatches
from app.models.messages import ChatRoom, UserMessages
from app.models.robots import *
from app.models.user import *

Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
