import os
from flask import send_from_directory
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import current_user
from werkzeug.utils import secure_filename
from app import app

app.config["UPLOADED_PHOTOS_DEST"] = f"app/static/images/users/current_user"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif"]
photos = UploadSet("photos", IMAGES)
configure_uploads(app, photos)

def get_image(photo, name="", url_path="users"):
    if name != "" and url_path != "users":
        app.config["UPLOADED_PHOTOS_DEST"] = f"app/static/images/{url_path}/{name}"
        os.makedirs(f"app/static/images/{url_path}/{name}", exist_ok=True)
    else:
        app.config["UPLOADED_PHOTOS_DEST"] = f"app/static/images/{url_path}/{current_user.name}"
        os.makedirs(f"app/static/images/{url_path}/{current_user.name}", exist_ok=True)
    
    filename = secure_filename(photo.filename)
    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return "Nieprawidłowe rozszerzenie pliku"
    photo.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], filename))
    return filename
    #file_url = url_for("get_file", filename=filename)


#@app.route("/uploads/<filename>", methods=["GET", "POST"])
#def get_file(filename):
#    return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)