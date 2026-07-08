from fastapi import FastAPI

SECRET_KEY = "123123!#!@123123#@!@31232145136"
ALGORITHM = "HS256"
ACCES_TOKEN_EXPIRE_DAYS = 365

app = FastAPI()

from app.dependencies import dependencies
from app.endpoints import endpoints
from app.dependencies.geolocation import geolocation
from app.schemas import schemas
from app.services.auth import auth
from app.services.database_operations import database_operations


