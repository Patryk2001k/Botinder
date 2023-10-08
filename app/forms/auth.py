from app.forms import *


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
            ("humanoid", "humanoid"),
            ("non-humanoid", "non-humanoid"),
            ("all", "all"),
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
        choices=[("male", "male"), ("female", "female"), ("custom", "custom")],
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
            ("working robot", "working robot"),
            ("disabled", "disabled"),
            ("all", "all"),
        ],
    )

    employment_status_profile = SelectField(
        "employment_status",
        validators=[DataRequired()],
        choices=[
            ("hired", "hired"),
            ("unemployed", "unemployed"),
            ("student", "student"),
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
