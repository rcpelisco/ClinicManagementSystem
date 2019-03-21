from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from cms.models import Medicine

class CreateDoctorScheduleForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    patient_id = SelectField('Patient', coerce=int)
    doctor_id = SelectField('Doctor', coerce=int)
    submit = SubmitField('Save Schedule')
 
class EditDoctorScheduleForm(CreateDoctorScheduleForm):
    id = IntegerField(widget=HiddenInput())
    