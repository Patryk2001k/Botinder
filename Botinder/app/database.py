import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()

DB_URL = os.environ.get(
    "DATABASE_URL", 
    "postgresql://botinder_user:botinder_secure_password@db:5432/botinder_web"
)

engine = create_engine(DB_URL, echo=True)

# Sprawdzenie istnienia bazy i wstrzyknięcie rozszerzeń PostGIS
if not database_exists(engine.url):
    create_database(engine.url)
    print("Database was created.")

with engine.connect() as connection:
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
    connection.commit()

Session = sessionmaker(bind=engine)
db_session = scoped_session(Session)

# Alias dla kompatybilności importów sesji
session = db_session

def init_db():
    """Importuje modele, aby zarejestrować je w metadanych Base, i tworzy tabele."""
    from app.models.chatroom import ChatRoom
    from app.models.matches import MatchBase, RobotMatches, UnMatches, UserMatches
    from app.models.messages import UserMessage
    from app.models.robots import RobotProfile, UserRobot
    from app.models.user import Profile, User, UserCriteria
    
    Base.metadata.create_all(bind=engine)