from pathlib import Path

from cryptography.fernet import Fernet
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from app.models import session
from app.models.user import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
destination_path = Path("app") / "static" / "images" / "users" / "current_user"
app.config["UPLOADED_PHOTOS_DEST"] = str(
    destination_path
)  # f"app/static/images/users/current_user"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif"]
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


from app import forms, routes, services, tests
from app.errors import handlers
from app.models import *
from app.routes import auth, routes
