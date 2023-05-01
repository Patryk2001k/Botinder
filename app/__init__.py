from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routes
from app import services
