from app.routes import *


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

            return redirect(url_for("user_homepage"))
        else:
            message = "Przykro mi ale masz nieprawidłowe dane"
            return render_template(
                "auth/register.html", form=form, register_failure_message=message
            )
    else:
        print(form.errors)
    return render_template("auth/register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserObject(form.username.data)
        user_log = get_user(form.username.data)
        user_admin = user.is_admin()
        if user.check_user_in_db_login(form.password.data) and not user_admin:
            login_user(user_log)

            return redirect(url_for("user_homepage"))

        elif user_admin:
            login_user(user_log)
            return redirect(url_for("admin_site"))

        else:
            return render_template(
                "auth/login.html",
                form=form,
                login_failure_message="Użytkownik nie istnieje",
            )

    elif not form.validate_on_submit() and form.submit_field.data:
        failure_message = "Przykro mi ale nie udało ci się zalogować, sprawdź proszę dane które wprowadziłeś "
        return render_template(
            "auth/login.html", form=form, login_failure_message=failure_message
        )

    else:
        return render_template("auth/login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    print(current_user.username)
    logout_user()
    return redirect(url_for("home"))
