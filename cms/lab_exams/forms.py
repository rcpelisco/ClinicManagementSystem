from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from cms.models import LabExam

class CreateLabExamForm(FlaskForm):
    stool_analysis = SelectField('Stool Analysis', 
        choices=[('normal', 'Normal'), ('abnormal', 'Abnormal')])
 
class EditLabExamForm(CreateLabExamForm):
    id = IntegerField(widget=HiddenInput())

class CreateCBCExamForm(FlaskForm):
    red_blood_cell_count = StringField('Red Blood Cell Count <br>(trillion cells/L)')
    white_blood_cell_count = StringField('White Blood Cell Count <br>(billion cells/L)')
    platelet_count = StringField('Platelet Count <br>(billion/L)')
    hemoglobin = StringField('Hemoglobin <br>(grams/dL)')
    hematocrit = StringField('Hematocrit <br>(percent)')

class EditCBCExamForm(CreateCBCExamForm):
    id = IntegerField(widget=HiddenInput())
    