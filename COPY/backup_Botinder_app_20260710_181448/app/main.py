from logging import basicConfig, getLogger  # JAWNE IMPORTY zamiast import logging
from flask import Flask
from flask_uploads import configure_uploads

from app.config import Config
from app.extensions import bcrypt, login_manager, socketio
from app.services.image_upload import photos
from app.database import db_session, init_db
from app.services.seeder import (
    seed_data,
)  # POPRAWKA (PEP 8): Import seeder-a na górze pliku
from app.routes.routes import main_bp
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.errors.handlers import errors_bp
from app.models.user import User  # POPRAWKA (PEP 8): Import modelu na górze pliku

# Konfiguracja logowania
basicConfig(
    level=20,  # Odpowiednik logging.INFO
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
getLogger("geocoder").setLevel(30)  # Odpowiednik logging.WARNING
getLogger("urllib3").setLevel(30)

logger = getLogger(__name__)


def create_app(config_class=Config):
    logger.info("Initializing Botinder application...")

    app = Flask(__name__)
    app.config.from_object(config_class)

    # Powiązanie rozszerzeń
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    # Powiązanie wtyczki przesyłania plików
    configure_uploads(app, photos)

    # Konfiguracja login managera
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    # Inicjalizacja tabel bazodanowych
    init_db()

    # Automatyczne zasianie danych testowych
    seed_data()

    # Automatyczne czyszczenie połączeń bazy danych po każdym żądaniu HTTP
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Rejestracja Blueprintów
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)

    logger.info("Botinder application started successfully.")
    return app


@login_manager.user_loader
def load_user(user_id):
    # POPRAWKA (PEP 8): Brak lokalnych importów, wszystko zdefiniowane na górze!
    return db_session.query(User).get(int(user_id))
