from logging import basicConfig, getLogger
from flask import Flask
from flask_uploads import configure_uploads

from app.config import Config
from app.extensions import bcrypt, login_manager, socketio
from app.services.image_upload import photos
from app.database import db_session, init_db
from app.services.seeder import seed_data
from app.routes.routes import main_bp
from app.routes.auth import auth_bp
from app.routes.admin import admin_bp
from app.errors.handlers import errors_bp
from app.models.user import User

basicConfig(level=20, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
getLogger("geocoder").setLevel(30)
getLogger("urllib3").setLevel(30)

logger = getLogger(__name__)


def create_app(config_class=Config):
    logger.info("Initializing Botinder application...")

    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    configure_uploads(app, photos)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."

    init_db()

    seed_data()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)

    logger.info("Botinder application started successfully.")
    return app


@login_manager.user_loader
def load_user(user_id):

    return db_session.query(User).get(int(user_id))
