from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists

Base = declarative_base()
metadata = MetaData()
DB_URL = "postgresql://postgres:admin@localhost/botinderapi"
engine = create_engine(DB_URL, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
    with engine.connect() as connection:
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))
        connection.execute(text('CREATE EXTENSION IF NOT EXISTS "postgis";'))
    print("Utworzono bazę danych.")


#importowanie tabel
from app.models.user import User

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
