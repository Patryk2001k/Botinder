from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from app.forms.utils import enum_to_choices
from app.models.enums import EmploymentStatusCriteria, RobotType


class AdminForm(FlaskForm):
    type_of_robot = SelectField(
        "type of robot",
        validators=[DataRequired()],
        choices=enum_to_choices(RobotType, replace=True),
    )

    name = StringField("name", validators=[DataRequired()])
    procesor_unit = StringField("procesor unit", validators=[DataRequired()])
    profile_description = TextAreaField("description", validators=[DataRequired()])

    employment_status = SelectField(
        "employment status",
        validators=[DataRequired()],
        choices=enum_to_choices(EmploymentStatusCriteria, replace=True),
    )

    domicile = StringField("domicile", validators=[DataRequired()])

    photo = FileField(
        validators=[
            FileAllowed(["jpg", "jpeg", "png"], "only images allowed"),
            FileRequired("File field should be empty"),
        ]
    )

    submit_field = SubmitField("Submit")
