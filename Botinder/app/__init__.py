import os
from pathlib import Path

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_uploads import configure_uploads  # POPRAWKA: Import konfiguratora
from huey import RedisHuey

from app.config import Config
from app.services.image_upload import photos  # POPRAWKA: Import zestawu zdjęć

# Inicjalizacja rozszerzeń (globalna, niepowiązana jeszcze z instancją aplikacji)
bcrypt = Bcrypt()
login_manager = LoginManager()
socketio = SocketIO()

# Huey inicjalizujemy globalnie, odczytując adres Redisa z konfiguracji środowiskowej
redis_url = os.environ.get("REDIS_URL", "redis://redis:6379/0")
huey = RedisHuey('botinder-tasks', url=redis_url)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Powiązanie rozszerzeń z nowo utworzoną instancją aplikacji
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    # POPRAWKA: Powiązanie wtyczki przesyłania plików z aplikacją
    configure_uploads(app, photos)

    # Konfiguracja managera logowania
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from app.models import session
        session.remove()

    # Rejestracja Blueprintów (Modułów aplikacji)
    from app.routes.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)

    return app

# Ładowacz użytkownika dla Flask-Login (dynamiczny import modeli zapobiega cyklicznym importom)
@login_manager.user_loader
def load_user(user_id):
    from app.models import session
    from app.models.user import User
    return session.query(User).get(int(user_id))