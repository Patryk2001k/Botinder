from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (
    EmailField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.forms.utils import enum_to_choices
from app.models.enums import (
    EmploymentStatusCriteria,
    EmploymentStatusProfile,
    Gender,
    RobotType,
)
from app.database import db_session
from app.models.user import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "confirm password", validators=[DataRequired(), EqualTo("password")]
    )

    type_of_robot = SelectField(
        "type of robot",
        validators=[DataRequired()],
        choices=enum_to_choices(RobotType, replace=True),
    )
    distance = IntegerField("distance", validators=[DataRequired()])

    employment_status_criteria = SelectField(
        "employment status criteria",
        validators=[DataRequired()],
        choices=enum_to_choices(EmploymentStatusCriteria, replace=True),
    )

    age = IntegerField("age", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])
    gender = SelectField(
        "gender",
        validators=[DataRequired()],
        choices=enum_to_choices(Gender, replace=True),
    )
    profile_description = TextAreaField(
        "profile description", validators=[DataRequired()]
    )

    domicile = StringField("domicile", validators=[DataRequired()])

    education = StringField("education", validators=[DataRequired()])
    employment_status_profile = SelectField(
        "employment status profile",
        validators=[DataRequired()],
        choices=enum_to_choices(EmploymentStatusProfile, replace=True),
    )

    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("File field should not be empty"),
        ]
    )
    submit_field = SubmitField("Join today")

    def validate_username(self, username):
        user = db_session.query(User).filter_by(username=username.data).first()
        if user:
            raise ValidationError("This username is already taken.")

        if username.data == self.name.data:
            raise ValidationError("Username and display name must be different.")

    def validate_name(self, name):
        user = db_session.query(User).filter_by(name=name.data).first()
        if user:
            raise ValidationError("A user with this display name already exists.")

    def validate_email(self, email):
        user = db_session.query(User).filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email address is already registered.")

    def validate_password(self, password):
        from app.extensions import bcrypt

        users = db_session.query(User).all()
        for user in users:
            if bcrypt.check_password_hash(user.password, password.data):
                raise ValidationError(
                    "For security reasons, this password cannot be used as it is already registered by another user."
                )

    def validate_domicile(self, domicile):
        from geopy.geocoders import Nominatim

        geolocator = Nominatim(user_agent="Botinder_App_Validation_Client_2026")
        try:
            location = geolocator.geocode(domicile.data, timeout=5)
            if not location:
                raise ValidationError(
                    "We couldn't find this city. Please enter a valid, existing city name."
                )
        except ValidationError:
            raise
        except Exception:

            pass


class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_field = SubmitField("Log in")
