from os import environ  # JAWNY IMPORT
from logging import getLogger  # JAWNY IMPORT
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy_utils import create_database, database_exists

logger = getLogger(__name__)

Base = declarative_base()

# POPRAWKA (PEP 8): Importujemy wszystkie modele na poziomie modułu pod obiektem Base
from app.models.chatroom import ChatRoom
from app.models.matches import MatchBase, RobotMatches, UnMatches, UserMatches
from app.models.messages import UserMessage
from app.models.robots import RobotProfile, UserRobot
from app.models.user import Profile, User, UserCriteria

DB_URL = environ.get(
    "DATABASE_URL",
    "postgresql://botinder_user:botinder_secure_password@db:5432/botinder",
)

engine = create_engine(DB_URL, echo=False)

if not database_exists(engine.url):
    create_database(engine.url)
    logger.info("Database did not exist. Successfully created a new one.")

with engine.connect() as connection:
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
    connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
    connection.commit()

Session = sessionmaker(bind=engine, expire_on_commit=False)
db_session = scoped_session(Session)

session = db_session


def init_db() -> None:
    """Tworzy tabele w bazie danych (wywoływane w fabryce aplikacji)."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database schemas and PostGIS extensions initialized.")
