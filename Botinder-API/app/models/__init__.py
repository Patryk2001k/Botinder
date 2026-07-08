import os
from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
metadata = MetaData()

# POPRAWKA: Próbujemy odczytać DB_URL, jeśli pusta - sprawdzamy DATABASE_URL, na końcu localhost
DB_URL = os.environ.get("DB_URL") or os.environ.get("DATABASE_URL") or "postgresql://botinder_user:botinder_secure_password@localhost:5432/botinder_api"

engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
        connection.commit() # POPRAWKA: Musimy zatwierdzić transakcję!
    print("Utworzono bazę danych.")

from app.models.user import User

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# Automatyczne tworzenie użytkownika 'botinder'
with Session() as db_session:
    user_exists = db_session.query(User).filter_by(username="botinder").first()
    if not user_exists:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])
        hashed = pwd_context.hash("botinderpassword")
        new_user = User(username="botinder", hashed_password=hashed, disabled=False)
        db_session.add(new_user)
        db_session.commit()
        print("Utworzono domyślnego użytkownika 'botinder' dla API.")