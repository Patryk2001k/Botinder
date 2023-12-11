from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from geoalchemy2.elements import WKTElement

from app import app
from app.forms.auth import LoginForm, RegistrationForm
from app.services.database_operations.database_operations import (
    UserObject, get_coordinates, get_user, insert_user_and_user_profile,
    session_scope)
from app.services.image_upload import get_image

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.username.data != form.name.data:
            user = UserObject(form.name.data)
            if not user.check_user_in_db_registration(form.password.data):
                image_name = get_image(form.photo.data, form.name.data)
                with session_scope() as session:
                    insert_user_and_user_profile(
                        form.username.data,
                        form.name.data,
                        form.lastname.data,
                        form.password.data,
                        form.email.data,
                        image_name,
                        form.age.data,
                        form.gender.data,
                        form.profile_description.data,
                        form.domicile.data,
                        form.education.data,
                        form.employment_status_profile.data,
                        form.type_of_robot.data,
                        form.distance.data,
                        form.employment_status_criteria.data,
                        session,
                    )

                    user = get_user(session, form.name.data)

                    login_user(user)
                    print(form.domicile.data)
                    print(type(form.domicile.data))
                    
                    domicile_longitude_and_latitude = get_coordinates(form.domicile.data)
                    longitude = domicile_longitude_and_latitude[1]
                    latitude = domicile_longitude_and_latitude[0]
                    domicile_location = WKTElement(
                        f"POINT({longitude} {latitude})", srid=4326
                    )
                    user.domicile_geolocation = domicile_location
                    session.commit()
                    return redirect(url_for("check_user_location"))
            else:
                flash("Przykro mi ale taki użytkownik już istnieje w bazie danych")
                return render_template("auth/register.html", form=form)
        elif form.username.data == form.name.data:
            flash("Error in username or name: Username and login field must be diffrent")
            return render_template("auth/register.html", form=form)
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"Error in {fieldName}: {err}")
    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserObject(form.name.data)
        with session_scope() as session:
            user_log = get_user(session, form.name.data)
            if user.check_user_in_db_login(form.password.data) and not user.is_admin():
                login_user(user_log)
                return redirect(url_for("check_user_location"))

            elif user.is_admin():
                login_user(user_log)
                return redirect(url_for("admin_site"))

            else:
                flash("Użytkownik nie istnieje")
                return render_template(
                    "auth/login.html",
                    form=form,
                )

    elif not form.validate_on_submit() and form.submit_field.data:
        flash(
            "Przykro mi ale nie udało ci się zalogować, sprawdź proszę dane które wprowadziłeś"
        )
        return render_template("auth/login.html", form=form)

    else:
        return render_template("auth/login.html", form=form)


@app.route("/check_user_location", methods=["GET", "POST"])
@login_required
def check_user_location():
    return render_template("auth/check_user_location/check_user_location.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))
