from main_module import app, bcrypt
from flask import render_template, redirect, url_for, session
from models.forms import LoginForm, RegistrationForm, AdminForm, UserCriteria, UserProfileForm
from models.database_operations import user_in_database, select_all_from_database, insert_user_and_user_profile
from models.database import User

site_session = session

@app.route("/")
@app.route("/home")
def home():
    username = site_session.get('logged_username')
    if username:
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
        if not user_in_database(form.username.data, form.password.data):
            site_session['username'] = form.username.data
            site_session['email'] = form.email.data
            site_session['password'] = form.password.data
            return redirect(url_for("user_profile"))
    return render_template("register_form.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if user_in_database(form.username.data, form.password.data):
            site_session["logged_username"] = form.username.data
            print(select_all_from_database(User))
            return redirect(url_for("user_homepage"))
        
        elif form.username.data == "admin" and form.username.data == "admin":
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

@app.route("/user_homepage")
def user_homepage():
    logged_user = site_session.get("logged_username")
    registered_user = site_session.get("username")
    if logged_user:
        return render_template("user_homepage.html", user=logged_user)
    elif registered_user:
        return render_template("user_homepage.html", user=registered_user)

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
        username = site_session.get("username")
        email = site_session.get("email")
        password = site_session.get("password")
        age = site_session.get("age")
        gender = site_session.get("gender")
        profile_description = site_session.get("profile_description")
        domicile = site_session.get("domicile")
        education = site_session.get("education")
        employment_status = site_session.get("employment_status")

        insert_user_and_user_profile(username, password, email, age, gender, profile_description, domicile, education, employment_status)    

        print(form.data)
        
        return redirect(url_for("user_homepage"))
    return render_template("user-criteria-form.html", form=form)

@app.route("/admin_site", methods=["GET", "POST"])
def admin_site():
    form = AdminForm()
    if form.validate_on_submit():
        print(form.data)
        return render_template("admin-site.html", form=form)
    return render_template("admin-site.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    site_session.pop("logged_username", None)
    return redirect(url_for("home"))


