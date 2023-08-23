from flask import redirect, render_template, request, session, url_for
from flask_login import UserMixin, current_user, login_required, login_user, logout_user

from app import app
from app.forms import AdminForm, LoginForm, RegistrationForm
from app.models import RobotProfile, User, UserRobot
from app.services.database_operations.database_operations import (
    UserObject,
    get_user,
    insert_into_robots_db,
    insert_user_and_user_profile,
    select_all_from_database,
    update_user_location,
)
from app.services.geolocalization_services.user_localization_and_distance import (
    country_name_to_code,
    generate_random_ip,
    get_cities,
    get_coordinates,
    get_location,
)
from app.services.image_upload import get_image
