from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import HiddenInput
from cms.models import Medicine

class CreateMedicineForm(FlaskForm):
    last_stocked = DateField('Last stocked', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    count = IntegerField('Count', validators=[DataRequired()])
    submit = SubmitField('Add Medicine')

class DeductMedicineForm(FlaskForm):
    count = IntegerField('Count', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
 
class EditMedicineForm(FlaskForm):
    id = IntegerField(widget=HiddenInput())
    name = StringField('Name', validators=[DataRequired(), Length(min=2)])
    count = IntegerField('Count', validators=[DataRequired()])
    submit = SubmitField('Save Changes')
    