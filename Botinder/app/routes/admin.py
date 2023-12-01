from flask import render_template
from flask_login import login_required

from app import app
from app.forms.forms import AdminForm
from app.services.database_operations.database_operations import (
    insert_into_robots_db, session_scope)
from app.services.image_upload import get_image


@app.route("/admin_site", methods=["GET", "POST"])
@login_required
def admin_site():
    form = AdminForm()
    if form.validate_on_submit():
        image_name = get_image(form.photo.data, form.name.data, "robots")
        with session_scope() as session:
            insert_into_robots_db(
                session,
                form.name.data,
                image_name,
                form.type_of_robot.data,
                form.profile_description.data,
                form.domicile.data,
                form.procesor_unit.data,
                form.employment_status.data,
            )

        return render_template(
            "auth/admin/admin-site.html",
            form=form,
            message="Udało się dodać użytkownika",
        )
    return render_template("auth/admin/admin-site.html", form=form)
