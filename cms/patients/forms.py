from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import HiddenInput
from cms.models import Patient

class CreatePatientForm(FlaskForm):
    first_name = StringField('First name',
        validators=[DataRequired(), Length(min=2)])
    last_name = StringField('Last name',
        validators=[DataRequired(), Length(min=2)])
    date_of_birth = StringField('Date of Birth',
        validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'Male'), 
        ('female', 'Female')])
    address = StringField('Address', validators=[DataRequired()])
    contact_no = StringField('Contact no', Length(min=9, max=9))
    submit = SubmitField('Add Patient')
 
class EditPatientForm(CreatePatientForm):
    id = IntegerField(widget=HiddenInput())
    submit = SubmitField('Save Changes')
