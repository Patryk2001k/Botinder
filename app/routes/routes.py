from app.routes import *


@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("user_homepage"))
    else:
        return render_template("main/start-page.html")


@app.route("/lore")
def lore():
    return render_template("main/lore.html")


@app.route("/FAQ")
def FAQ_site():
    return render_template("main/FAQ.html")


"""
@app.route("/user_homepage", methods=["GET", "POST"])
def user_homepage():
    logout_user()
    return redirect(url_for("home"))
"""


@app.route("/user_homepage", methods=["GET"])
@login_required
def user_homepage():
    print(current_user.username)
    return render_template("user_homepage.html", user=current_user.name)


@app.route("/get_geolocation", methods=["POST"])
@login_required
def get_geolocation():
    data = request.get_json()
    print(current_user.username)

    latitude = data.get("latitude")
    longitude = data.get("longitude")
    print(f"{latitude}, {longitude}")

    update_user_location(longitude, latitude, current_user)
    user = get_user(current_user.username)
    print(user)
    return redirect(url_for("user_homepage"))


@app.route("/admin_site", methods=["GET", "POST"])
@login_required
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
            "auth/admin/admin-site.html",
            form=form,
            message="Udało się dodać użytkownika",
        )
    return render_template("auth/admin/admin-site.html", form=form)
