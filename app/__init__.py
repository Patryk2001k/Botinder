from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SECRET_KEY"] = "12342132542@#242@4%891"
bcrypt = Bcrypt(app)

from app import routes
from app import find_new_person