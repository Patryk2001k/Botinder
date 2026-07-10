import logging
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from geoalchemy2.elements import WKTElement

from app.forms.auth import LoginForm, RegistrationForm
from app.services.database_operations import get_user, insert_user_and_user_profile, session_scope

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    from app.services.geolocalization import GeolocalizationService
    from app.services.image_upload import get_image

    form = RegistrationForm()
    if form.validate_on_submit():
        logger.info(f"Attempting to register user: {form.username.data}")
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

            # POPRAWKA: Pobieramy nowo zarejestrowanego użytkownika po jego unikalnym LOGINIE (username)
            user = get_user(session, form.username.data)
            login_user(user)
            
            domicile_longitude_and_latitude = GeolocalizationService.get_coordinates(form.domicile.data)
            longitude = domicile_longitude_and_latitude[1]
            latitude = domicile_longitude_and_latitude[0]
            domicile_location = WKTElement(
                f"POINT({longitude} {latitude})", srid=4326
            )
            user.domicile_geolocation = domicile_location
            session.commit()
            
            logger.info(f"User {form.username.data} registered and logged in successfully.")
            return redirect(url_for("auth.check_user_location"))
    else:
        if form.is_submitted():
            logger.warning(f"Registration validation failed. Errors: {form.errors}")
            
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f"Error in {fieldName}: {err}")
                
    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    from app.services.database_operations import UserObject
    
    form = LoginForm()
    if form.validate_on_submit():
        # POPRAWKA: Logowanie oparte na unikalnym LOGINIE (form.username.data)
        logger.info(f"User {form.username.data} is attempting to log in.")
        user = UserObject(form.username.data)
        
        with session_scope() as session:
            user_log = get_user(session, form.username.data)
            if user.check_user_in_db_login(form.password.data) and not user.is_admin():
                login_user(user_log)
                logger.info(f"User {form.username.data} logged in successfully.")
                return redirect(url_for("auth.check_user_location"))

            elif user.is_admin():
                login_user(user_log)
                logger.info(f"Administrator {form.username.data} logged in successfully.")
                return redirect(url_for("admin.admin_site"))

            else:
                logger.warning(f"Failed login attempt for user: {form.username.data} (User does not exist or wrong password).")
                flash("Użytkownik nie istnieje")
                return render_template("auth/login.html", form=form)

    elif not form.validate_on_submit() and form.submit_field.data:
        logger.warning("Login form submission rejected due to form validation errors.")
        flash("Przykro mi ale nie udało ci się zalogować, sprawdź proszę dane które wprowadziłeś")
        return render_template("auth/login.html", form=form)

    return render_template("auth/login.html", form=form)


@auth_bp.route("/check_user_location", methods=["GET", "POST"])
@login_required
def check_user_location():
    return render_template("auth/check_user_location/check_user_location.html")


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    logger.info(f"User logged out.")
    logout_user()
    return redirect(url_for("main.home"))