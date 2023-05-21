from flask import redirect, render_template, request, session, url_for
from flask_login import (UserMixin, current_user, login_required, login_user,
                         logout_user)

from app import app, cipher_suite, login_manager
from app.get_image import get_image
from app.user_localization_and_distance import (country_name_to_code,
                                                generate_random_ip, get_cities,
                                                get_location)
from models.database import RobotProfile, User, UserRobot
from models.database_operations import (get_user_from_User_table,
                                        if_user_is_admin,
                                        insert_into_robots_db,
                                        insert_user_and_user_profile,
                                        select_all_from_database,
                                        user_in_database)
from models.forms import (AdminForm, LoginForm, RegistrationForm, UploadForm,
                          UserCriteria, UserProfileForm)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

site_session = session

@app.route("/")
@app.route("/home")
def home():
    # print(get_location())
    # print(country_name_to_code())
    #print(get_cities())
    # x = country_name_to_code("Poland")
    # print(x)
    # print(get_cities(x))
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage"))
    else:
        return render_template("start-page.html")


@app.route("/lore")
def lore():
    return render_template("lore.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if not user_in_database(form.password.data):
            user_password = form.password.data
            site_session["name"] = form.name.data
            site_session["lastname"] = form.lastname.data
            site_session["email"] = form.email.data
            site_session["password"] = cipher_suite.encrypt(user_password.encode())
            return redirect(url_for("user_profile"))
        else:
            message = "Przykro mi ale masz nieprawidłowe dane"
            return render_template(
                "register_form.html", form=form, register_failure_message=message
            )
    return render_template("register_form.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user_in_database(form.password.data) and if_user_is_admin(
            form.name.data, form.password.data
        ):
            user = get_user_from_User_table(form.name.data)
            login_user(user)
            print(current_user.name)
            return redirect(url_for("user_homepage"))

        elif if_user_is_admin(form.name.data, form.password.data):
            return redirect(url_for("admin_site"))

        else:
            return render_template(
                "login.html", form=form, login_failure_message="Użytkownik nie istnieje"
            )

    elif not form.validate_on_submit() and form.submit_field.data:
        failure_message = "Przykro mi ale nie udało ci się zalogować, sprawdź proszę dane które wprowadziłeś "
        return render_template(
            "login.html", form=form, login_failure_message=failure_message
        )

    else:
        return render_template("login.html", form=form)


@app.route("/FAQ")
def FAQ_site():
    return render_template("FAQ.html")


@app.route("/user_profile", methods=["GET", "POST"])
def user_profile():
    form = UserProfileForm()
    if form.validate_on_submit():
        site_session["age"] = form.age.data
        site_session["gender"] = form.gender.data
        site_session["profile_description"] = form.profile_description.data
        site_session["domicile"] = form.domicile.data
        site_session["education"] = form.education.data
        site_session["employment_status"] = form.employment_status.data

        return redirect(url_for("user_criteria"))

    elif not form.validate_on_submit() and form.submit_field.data:
        failure_message = "Przykro mi ale nie udało ci się poprawnie wypełnić formularza, spróbuj ponownie"
        return render_template(
            "user-information-form.html", form=form, failure_message=failure_message
        )

    else:
        return render_template("user-information-form.html", form=form)


@app.route("/user_criteria", methods=["GET", "POST"])
def user_criteria():
    form = UserCriteria()
    if form.validate_on_submit():
        site_session["type_of_robot"] = form.type_of_robot.data
        site_session["distance"] = form.distance.data
        site_session["employment_status_criteria"] = form.employment_status.data

        return redirect(url_for("get_main_image"))
    return render_template("user-criteria-form.html", form=form)


@app.route("/get_main_image", methods=["GET", "POST"])
def get_main_image():
    form = UploadForm()
    if form.validate_on_submit():
        name = site_session.get("name")
        lastname = site_session.get("lastname")
        email = site_session.get("email")

        password = site_session.get("password")
        user_password_decrypted = cipher_suite.decrypt(password)
        user_password_decoded = user_password_decrypted.decode("utf-8")

        age = site_session.get("age")
        gender = site_session.get("gender")
        profile_description = site_session.get("profile_description")
        domicile = site_session.get("domicile")
        education = site_session.get("education")
        employment_status = site_session.get("employment_status")
        type_of_robot = site_session.get("type_of_robot")
        distance = site_session.get("distance")
        employment_status_criteria = site_session.get("employment_status_criteria")

        image_name = get_image(form.photo.data, name)

        insert_user_and_user_profile(
            name,
            lastname,
            user_password_decoded,
            email,
            image_name,
            age,
            gender,
            profile_description,
            domicile,
            education,
            employment_status,
            type_of_robot,
            distance,
            employment_status_criteria,
        )

        user = get_user_from_User_table(name)

        login_user(user)

        session.pop("name", None)
        session.pop("lastname", None)
        session.pop("email", None)
        session.pop("password", None)
        session.pop("age", None)
        session.pop("gender", None)
        session.pop("profile_description", None)
        session.pop("domicile", None)
        session.pop("education", None)
        session.pop("employment_status", None)
        session.pop("type_of_robot", None)
        session.pop("distance", None)
        session.pop("employment_status_criteria", None)

        return redirect(url_for("user_homepage"))
    return render_template("get-main-image.html", form=form)


@app.route("/user_homepage")
@login_required
def user_homepage():
    print(current_user.name)
    if current_user.is_authenticated:
        return render_template("user_homepage.html", user=current_user.name)


@app.route("/admin_site", methods=["GET", "POST"])
def admin_site():
    form = AdminForm()
    if form.validate_on_submit():
        print(form.name.data)
        print(form.type_of_robot.data)
        image_name = get_image(form.photo.data, form.name.data, "robots")
        insert_into_robots_db(
            form.name.data,
            image_name,
            form.type_of_robot.data,
            form.profile_description.data,
            form.domicile.data,
            form.procesor_unit.data,
            form.employment_status.data,
        )
        print(select_all_from_database(UserRobot))
        print("-----------")
        print(select_all_from_database(RobotProfile))

        return render_template(
            "admin-site.html", form=form, message="Udało się dodać użytkownika"
        )
    return render_template("admin-site.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    print(current_user.name)
    logout_user()
    return redirect(url_for("home"))
