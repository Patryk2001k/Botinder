from os import environ
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


load_dotenv(dotenv_path=BASE_DIR / ".env")


class Config:

    SECRET_KEY = environ.get("SECRET_KEY", "12342132542@#242@4%891")

    UPLOADED_PHOTOS_DEST = environ.get(
        "UPLOADED_PHOTOS_DEST",
        str(BASE_DIR / "app" / "static" / "images" / "users" / "current_user"),
    )
    ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif"]
    STATIC_USER_IP = ""

    DATABASE_URL = environ.get(
        "DATABASE_URL",
        "postgresql://botinder_user:botinder_secure_password@db:5432/botinder_web",
    )

    REDIS_URL = environ.get("REDIS_URL", "redis://redis:6379/0")
