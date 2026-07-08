import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "12342132542@#242@4%891")
    
    # Ścieżki
    BASE_DIR = Path(__file__).resolve().parent.parent
    UPLOADED_PHOTOS_DEST = os.environ.get(
        "UPLOADED_PHOTOS_DEST", 
        str(BASE_DIR / "app" / "static" / "images" / "users" / "current_user")
    )
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
    STATIC_USER_IP = ""
    
    # Baza danych
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", 
        "postgresql://botinder_user:botinder_secure_password@db:5432/botinder_web"
    )
    
    # Redis i Huey
    REDIS_URL = os.environ.get("REDIS_URL", "redis://redis:6379/0")
    
    # Botinder API
    BOTINDER_API_URL = os.environ.get("BOTINDER_API_URL", "http://botinder-api:8000")
    BOTINDER_API_LOGIN_DATA = {"username": "botinder", "password": "botinderpassword"}