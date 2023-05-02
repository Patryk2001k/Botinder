import os
from flask import send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from werkzeug.utils import secure_filename
from app import app, UploadForm

os.makedirs("app/static/images/current_user", exist_ok=True)
app.config["UPLOADED_PHOTOS_DEST"] = "app/static/images/current_user"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif"]
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

def get_image(photo):
    filename = secure_filename(photo.filename)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return "Invalid file extension. Please select a valid image file."
    photo.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], filename))
    file_url = url_for("get_file", filename=filename)


@app.route("/uploads/<filename>", methods=["GET", "POST"])
def get_file(filename):
    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)