from flask_wtf import FlaskForm
from cms.models import MedicalRecord
from wtforms import SelectMultipleField 
from wtforms import StringField, SubmitField, IntegerField, DecimalField
from wtforms.widgets import HiddenInput
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""

class CreateMedicalRecordForm(FlaskForm):
    patient_id = IntegerField(widget=HiddenInput())
    symptom = NoValidationSelectMultipleField('Symptom', coerce=str)
    weight = DecimalField('Weight (kg)', validators=[DataRequired()])
    height = DecimalField('Height (cm)', validators=[DataRequired()])
    temperature = DecimalField('Temperature (&#176;C)', 
        validators=[DataRequired()])
    finding = StringField('Finding', validators=[DataRequired(), Length(min=2)])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Save Medical Record')
 
class EditMedicalRecordForm(CreateMedicalRecordForm):
    id = IntegerField(widget=HiddenInput())
    