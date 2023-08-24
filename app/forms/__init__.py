from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms.auth import LoginForm, RegistrationForm
from app.forms.forms import AdminForm
from app.services.geolocalization_services.user_localization_and_distance import (
    get_cities,
)
