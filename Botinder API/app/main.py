from fastapi import FastAPI

app = FastAPI()

from app.dependencies import dependencies
from app.endpoints import endpoints
from app.dependencies.geolocation import geolocation


