from cryptography.fernet import Fernet
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.models import User, Session

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
cipher_suite = Fernet(Fernet.generate_key())

@login_manager.user_loader
def load_user(user_id):
    session = Session()
    return session.query(User).get(int(user_id))

from app import routes, services
from app.errors import handlers
