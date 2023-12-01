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

from app.forms.enums import (
    EmploymentStatusCriteria,
    EmploymentStatusProfile,
    Gender,
    RobotType,
)
from app.services.geolocalization_services.user_localization_and_distance import (
    get_cities,
)


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
        choices=[
            (str(robot_type).replace("_", "-"), str(robot_type.value))
            for robot_type in RobotType
        ],
    )

    distance = IntegerField(
        "distance (How far away should the robot live in km)",
        validators=[DataRequired()],
    )

    age = IntegerField("age", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])

    gender = SelectField(
        "gender",
        validators=[DataRequired()],
        choices=[(str(Gender), str(Gender.value)) for Gender in Gender],
    )

    profile_description = TextAreaField("description", validators=[DataRequired()])

    domicile = SelectField(
        "domicile", validators=[DataRequired()], choices=[(i, i) for i in get_cities()]
    )

    education = StringField("education", validators=[DataRequired()])

    employment_status_criteria = SelectField(
        "employment status",
        validators=[DataRequired()],
        choices=[
            (str(employment).replace("_", " "), str(employment.value))
            for employment in EmploymentStatusCriteria
        ],
    )

    employment_status_profile = SelectField(
        "employment_status",
        validators=[DataRequired()],
        choices=[
            (str(employment), str(employment.value))
            for employment in EmploymentStatusProfile
        ],
    )

    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("Please upload a file"),
        ]
    )

    submit_field = SubmitField("Submit")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )

    password = PasswordField("Password", validators=[DataRequired()])
    submit_field = SubmitField("Login")
