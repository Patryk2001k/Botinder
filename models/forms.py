from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (BooleanField, IntegerField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.user_localization_and_distance import get_cities


class RegistrationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])

    lastname = StringField(
        "Lastname", validators=[DataRequired(), Length(min=2, max=40)]
    )

    email = StringField("Email", validators=[DataRequired(), Email()])

    password = PasswordField("Password", validators=[DataRequired()])

    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    submit_field = SubmitField("Submit")


class LoginForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(min=2, max=20)])

    password = PasswordField("Password", validators=[DataRequired()])

    submit_field = SubmitField("Login")


class UserProfileForm(FlaskForm):
    age = IntegerField("age", validators=[DataRequired()])

    gender = SelectField(
        "gender",
        validators=[DataRequired()],
        choices=[("male", "male"), ("female", "female"), ("custom", "custom")],
    )

    profile_description = TextAreaField("description", validators=[DataRequired()])

    domicile = SelectField(
        "domicile", validators=[DataRequired()], choices=[(i, i) for i in get_cities()]
    )

    education = StringField("education", validators=[DataRequired()])

    employment_status = SelectField(
        "employment_status",
        validators=[DataRequired()],
        choices=[
            ("hired", "hired"),
            ("unemployed", "unemployed"),
            ("student", "student"),
        ],
    )

    submit_field = SubmitField("Submit")


class UserCriteria(FlaskForm):
    type_of_robot = SelectField(
        "type of robot",
        validators=[DataRequired()],
        choices=[("humanoid"), ("non-humanoid"), ("all")],
    )

    distance = IntegerField(
        "distance (How far away should the robot live in km)",
        validators=[DataRequired()],
    )

    employment_status = SelectField(
        "employment status",
        validators=[DataRequired()],
        choices=[("working robot"), ("disabled"), ("all")],
    )

    submit_field = SubmitField("Submit")


class AdminForm(FlaskForm):
    type_of_robot = SelectField(
        "type of robot",
        validators=[DataRequired()],
        choices=[("humanoid"), ("non-humanoid"), ("all")],
    )

    name = StringField("name", validators=[DataRequired()])

    procesor_unit = StringField("procesor unit", validators=[DataRequired()])

    profile_description = TextAreaField("description", validators=[DataRequired()])

    employment_status = SelectField(
        "employment status",
        validators=[DataRequired()],
        choices=[("working robot"), ("disabled"), ("all")],
    )

    domicile = StringField("domicile", validators=[DataRequired()])

    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("File field should be empty"),
        ]
    )

    submit_field = SubmitField("Submit")


class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("File field should be empty"),
        ]
    )
    submit_field = SubmitField("Submit")
