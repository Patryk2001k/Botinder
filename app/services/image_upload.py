import os

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet, configure_uploads
from werkzeug.utils import secure_filename

from app import app

photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)


def get_image(photo, name, url_path="users"):
    app.config["UPLOADED_PHOTOS_DEST"] = f"app/static/images/{url_path}/{name}"
    os.makedirs(f"app/static/images/{url_path}/{name}", exist_ok=True)

    filename = secure_filename(photo.filename)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return "Nieprawidłowe rozszerzenie pliku"
    photo.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], filename))
    print(filename)
    return filename
    # file_url = url_for("get_file", filename=filename)


# @app.route("/uploads/<filename>", methods=["GET", "POST"])
# def get_file(filename):
#    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)
