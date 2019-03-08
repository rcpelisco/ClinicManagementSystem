from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from cms.models import User

POSITION_CHOICES = [('doctor', 'Doctor'), ('nurse', 'Nurse')]

class RegistrationForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2)])
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2)])
    position = SelectField('Position', choices=POSITION_CHOICES,
        validators=[])
    password = PasswordField('Password',
        validators=[DataRequired(), Length(min=3)])
    confirm_password = PasswordField('Confirm Password',
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose another one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=2)])
    password = PasswordField('Password',
        validators=[DataRequired()])
    submit = SubmitField('Login')