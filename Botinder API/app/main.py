from fastapi import FastAPI

SECRET_KEY = "123123!#!@123123#@!@31232145136"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_DAYS = 365

app = FastAPI()

from app.services.auth.auth import create_user, get_user_by_username, get_password_hash

#create_user("botinder", get_password_hash("botinderpassword"), False)
#print(get_user_by_username("botinder"))

from app.dependencies import dependencies
from app.endpoints import endpoints
from app.dependencies.geolocation import geolocation
from app.schemas import schemas
from app.services.auth import auth
from app.services.database_operations import database_operations


