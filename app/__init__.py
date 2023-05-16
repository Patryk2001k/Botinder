from cryptography.fernet import Fernet
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
cipher_suite = Fernet(Fernet.generate_key())

from app import routes, services
