from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (IntegerField, PasswordField, SelectField, StringField,
                     SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms.utils import enum_to_choices
from app.models.enums import (EmploymentStatusCriteria,
                              EmploymentStatusProfile, Gender, RobotType)
from app.services.geolocalization_services.user_localization_and_distance import \
    get_cities


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    type_of_robot = SelectField(
        "type of robot",
        validators=[DataRequired()],
        choices=enum_to_choices(RobotType, replace=True),
    )

    distance = IntegerField(
        "distance (How far away should the robot live in km)",
        validators=[DataRequired()],
    )

    age = IntegerField("age", validators=[DataRequired()])
    name = StringField("login (must be diffrent from username field)", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])

    gender = SelectField(
        "gender",
        validators=[DataRequired()],
        choices=enum_to_choices(Gender, replace=False),
    )

    profile_description = TextAreaField("description", validators=[DataRequired()])

    domicile = SelectField(
        "domicile", validators=[DataRequired()], choices=[(i, i) for i in get_cities()]
    )

    education = StringField("education", validators=[DataRequired()])

    employment_status_criteria = SelectField(
        "employment status",
        validators=[DataRequired()],
        choices=enum_to_choices(EmploymentStatusCriteria, replace=True),
    )

    employment_status_profile = SelectField(
        "employment_status",
        validators=[DataRequired()],
        choices=enum_to_choices(EmploymentStatusProfile, replace=False),
    )

    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("Please upload a file"),
        ]
    )

    submit_field = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField("Login", validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField("Password", validators=[DataRequired()])
    submit_field = SubmitField("Login")
