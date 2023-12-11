from pathlib import Path

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from huey import SqliteHuey

from app.services.API_requests.requests import get_botinderAPI_token

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
destination_path = Path("app") / "static" / "images" / "users" / "current_user"
app.config["UPLOADED_PHOTOS_DEST"] = str(destination_path)
app.config["ALLOWED_IMAGE_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif"]
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)
huey = SqliteHuey("Botinder")
BOTINDER_API_URL = "http://127.0.0.1:8000"
BOTINDER_API_LOGIN_DATA = {"username": "botinder", "password": "APIpassword:)"}
BOTINDER_API_TOKEN = get_botinderAPI_token(BOTINDER_API_URL, BOTINDER_API_LOGIN_DATA)
BOTINDER_API_HEADERS = {"Authorization": f"Bearer {BOTINDER_API_TOKEN}"}


from app import forms, routes, services, tests
from app.errors import handlers
from app.models import *
from app.routes import admin, auth, routes


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))