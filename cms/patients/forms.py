from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from cms.models import Patient

class CreatePatientForm(FlaskForm):
    name = StringField('Name',
        validators=[DataRequired(), Length(min=2)])
    date_of_birth = DateField('Date of Birth',
        validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Add Patient')

    def validate_name(self, name):
        patient = Patient.query.filter_by(name=name.data).first()
        if patient:
            raise ValidationError('Name is already taken. Please choose another one.')