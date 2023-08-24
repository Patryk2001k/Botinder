from app.forms import *


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
