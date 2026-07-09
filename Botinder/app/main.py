from flask import Flask
from flask_uploads import configure_uploads

from app.config import Config
from app.extensions import bcrypt, login_manager, socketio
from app.services.image_upload import photos
from app.database import db_session, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Powiązanie rozszerzeń
    bcrypt.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)
    
    # Powiązanie wtyczki przesyłania plików
    configure_uploads(app, photos)

    # Konfiguracja login managera
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'

    # Inicjalizacja tabel bazodanowych
    init_db()

    # Automatyczne czyszczenie połączeń bazy danych po każdym żądaniu HTTP
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # Rejestracja Blueprintów bezpośrednio z ich plików modułowych
    from app.routes.routes import main_bp
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.errors.handlers import errors_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(errors_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    from app.models.user import User
    from app.database import db_session
    return db_session.query(User).get(int(user_id))