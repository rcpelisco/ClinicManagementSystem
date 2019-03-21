from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, DecimalField, SelectMultipleField 
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from cms.models import MedicalRecord

class NoValidationSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        """per_validation is disabled"""

class CreateMedicalRecordForm(FlaskForm):
    patient_id = IntegerField(widget=HiddenInput())
    symptom = NoValidationSelectMultipleField('Symptom', coerce=str)
    weight = DecimalField('Weight', validators=[DataRequired()])
    height = DecimalField('Height', validators=[DataRequired()])
    bp = StringField('Blood Pressure', validators=[DataRequired(), 
        Length(min=2)])
    finding = StringField('Finding', validators=[DataRequired(), Length(min=2)])
    date = DateField('Date', validators=[DataRequired()])
    submit = SubmitField('Save Medical Record')
 
class EditMedicalRecordForm(CreateMedicalRecordForm):
    id = IntegerField(widget=HiddenInput())
    