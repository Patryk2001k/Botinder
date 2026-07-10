from os import environ  # JAWNY IMPORT zamiast import os
from pathlib import Path  # JAWNY IMPORT
from dotenv import load_dotenv  # JAWNY IMPORT

# Dynamiczne określenie głównego katalogu aplikacji Botinder
BASE_DIR = Path(__file__).resolve().parent.parent

# Bezpieczne wczytanie zmiennych z pliku .env (jeśli fizycznie istnieje na dysku)
load_dotenv(dotenv_path=BASE_DIR / ".env")

class Config:
    # Pobieramy konfiguracje z systemu (Docker lub plik .env) z bezpiecznym fallbackiem
    SECRET_KEY = environ.get("SECRET_KEY", "12342132542@#242@4%891")
    
    # Ścieżki
    UPLOADED_PHOTOS_DEST = environ.get(
        "UPLOADED_PHOTOS_DEST", 
        str(BASE_DIR / "app" / "static" / "images" / "users" / "current_user")
    )
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
    STATIC_USER_IP = ""
    
    # Baza danych
    DATABASE_URL = environ.get(
        "DATABASE_URL", 
        "postgresql://botinder_user:botinder_secure_password@db:5432/botinder_web"
    )
    
    # Redis i Huey
    REDIS_URL = environ.get("REDIS_URL", "redis://redis:6379/0")
    
    # Botinder API
    BOTINDER_API_URL = environ.get("BOTINDER_API_URL", "http://127.0.0.1:8000")
    BOTINDER_API_LOGIN_DATA = {"username": "botinder", "password": "botinderpassword"}