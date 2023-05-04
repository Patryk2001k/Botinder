from app import app, login_manager
from flask import render_template, redirect, url_for, session
from models.forms import LoginForm, RegistrationForm, AdminForm, UserCriteria, UserProfileForm, UploadForm
from models.database_operations import (
    user_in_database,
    select_all_from_database,
    insert_user_and_user_profile,
    insert_into_robots_db,
    get_user_from_User_table
)
from models.database import User, UserRobot, RobotProfile
from flask_login import UserMixin, login_user, logout_user, login_required, current_user
from app.get_image import get_image

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


site_session = session

@app.route("/")
@app.route("/home")
def home():
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
        if not user_in_database(form.name.data, form.password.data):
            site_session['name'] = form.name.data
            site_session['lastname'] = form.lastname.data
            site_session['email'] = form.email.data
            site_session['password'] = form.password.data
            return redirect(url_for("user_profile"))
    return render_template("register_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user_in_database(form.name.data, form.password.data):
            user = get_user_from_User_table(form.name.data)
            login_user(user)
            print(current_user.name)
            return redirect(url_for("user_homepage"))
        
        elif form.name.data == "admin" and form.password.data == "admin@42141412admin":
            return redirect(url_for("admin_site"))

        else:
            return render_template("login.html", form=form, login_failure_message="Użytkownik nie istnieje")
    
    elif not form.validate_on_submit() and form.submit_field.data:
        failure_message = "Przykro mi ale nie udało ci się zalogować, sprawdź proszę dane które wprowadziłeś "
        return render_template("login.html", form=form, login_failure_message=failure_message)
    
    else:
        return render_template("login.html", form=form)

@app.route("/FAQ")
def FAQ_site():
    return render_template("FAQ.html")

@app.route("/user_profile", methods=["GET" ,"POST"])
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
        return render_template("user-information-form.html", form=form, failure_message=failure_message)
    
    else:
        return render_template("user-information-form.html", form=form)

@app.route("/user_criteria", methods=["GET", "POST"])
def user_criteria():
    form = UserCriteria()
    if form.validate_on_submit():      
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
        age = site_session.get("age")
        gender = site_session.get("gender")
        profile_description = site_session.get("profile_description")
        domicile = site_session.get("domicile")
        education = site_session.get("education")
        employment_status = site_session.get("employment_status")

        
        insert_user_and_user_profile(name, lastname, password, email, age, gender, profile_description, domicile, education, employment_status)    
        
        user = get_user_from_User_table(name)

        login_user(user)

        get_image(form.photo.data)
        
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
        print(form.data)
        insert_into_robots_db(
            form.name.data,
            form.type_of_robot.data,
            form.profile_description.data,
            form.domicile.data,
            form.procesor_unit.data,
            form.employment_status.data
        )
        select_all_from_database(UserRobot)
        print("-----------")
        select_all_from_database(RobotProfile)
        return render_template("admin-site.html", form=form, message="Udało się dodać użytkownika")
    return render_template("admin-site.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    print(current_user.name)
    logout_user()
    return redirect(url_for("home"))


