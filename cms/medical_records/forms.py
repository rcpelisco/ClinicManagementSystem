from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from cms.models import MedicalRecord

class CreateMedicalRecordForm(FlaskForm):
    patient_id = IntegerField(widget=HiddenInput())
    symptom = StringField('Symptom',
        validators=[DataRequired(), Length(min=2)])
    finding = StringField('Finding',
        validators=[DataRequired(), Length(min=2)])
    submit = SubmitField('Save Medical Record')
 
class EditMedicalRecordForm(CreateMedicalRecordForm):
    id = IntegerField(widget=HiddenInput())
    