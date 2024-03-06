import os
import secrets

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet, configure_uploads

from app import app

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)


def get_image(photo, name, url_path="users"):
    app.config["UPLOADED_PHOTOS_DEST"] = f"app/static/images/{url_path}/{name}"
    os.makedirs(f"app/static/images/{url_path}/{name}", exist_ok=True)

    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(photo.filename)
    picture_fn = random_hex + f_ext

    if f_ext not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return "Nieprawidłowe rozszerzenie pliku"

    photo.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], picture_fn))
    return picture_fn
