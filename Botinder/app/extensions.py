import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from huey import RedisHuey

# Czysta deklaracja rozszerzeń
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

# Huey pobiera adres Redisa z konfiguracji środowiskowej
redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
huey = RedisHuey('botinder-tasks', url=redis_url)