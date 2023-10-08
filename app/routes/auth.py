from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app
from app.forms.auth import LoginForm, RegistrationForm
from app.services.database_operations.database_operations import (
    UserObject,
    get_user,
    insert_user_and_user_profile,
)
from app.services.image_upload import get_image


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserObject(form.username.data)
        if not user.check_user_in_db_registration(form.password.data):
            image_name = get_image(form.photo.data, form.name.data)

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
            )

            user = get_user(form.username.data)

            login_user(user)

            return redirect(url_for("check_user_location"))
        else:
            flash("Przykro mi ale masz nieprawidłowe dane")
            return render_template("auth/register.html", form=form)
    else:
        print(form.errors)
    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserObject(form.username.data)
        user_log = get_user(form.username.data)
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
