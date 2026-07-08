from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import (EmailField, IntegerField, PasswordField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app.forms.utils import enum_to_choices
from app.models.enums import EmploymentStatusProfile, Gender, RobotType
# POPRAWKA: Import nowego serwisu
from app.services.geolocalization import GeolocalizationService

class RegistrationForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("email", validators=[DataRequired(), Email()])
    password = PasswordField("password", validators=[DataRequired()])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password")])
    
    type_of_robot = SelectField("type of robot", validators=[DataRequired()], choices=enum_to_choices(RobotType, replace=True))
    distance = IntegerField("distance", validators=[DataRequired()])
    
    from app.models.enums import EmploymentStatusCriteria
    employment_status_criteria = SelectField("employment status criteria", validators=[DataRequired()], choices=enum_to_choices(EmploymentStatusCriteria, replace=True))
    
    age = IntegerField("age", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])
    lastname = StringField("lastname", validators=[DataRequired()])
    gender = SelectField("gender", validators=[DataRequired()], choices=enum_to_choices(Gender, replace=True))
    profile_description = TextAreaField("profile description", validators=[DataRequired()])
    
    domicile = SelectField("domicile", validators=[DataRequired()])
    
    education = StringField("education", validators=[DataRequired()])
    employment_status_profile = SelectField("employment status profile", validators=[DataRequired()], choices=enum_to_choices(EmploymentStatusProfile, replace=True))
    
    photo = FileField(validators=[FileAllowed(["jpg", "jpeg", "png"], "only images allowed"), FileRequired("File field should not be empty")])
    submit_field = SubmitField("Join today")

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.domicile.choices = [(city, city) for city in GeolocalizationService.get_cities()]


class LoginForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit_field = SubmitField("Log in")