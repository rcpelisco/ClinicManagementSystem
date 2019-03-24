from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from datetime import date, datetime
from cms import db
from cms.models import RecordSchema
from cms.models import MedicalRecord

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('patients.index'))

@dashboard.route('/all', methods=['GET', 'POST'])
def month():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = RecordSchema(many=True, only=['findings', 'patient'])

    output = medical_records_schema.dump(medical_records).data
    for record in output:
        record['id'] = record['findings']['id']
        record['findings'] = record['findings']['findings']
        record['gender'] = 1 if record['patient']['gender'] == 'Male' else 2
        record['age'] = calculate_age(record['patient']['date_of_birth'])
        del(record['patient'])
        print(record)
    return jsonify(output)
    return redirect(url_for('patients.index'))

def calculate_age(date_of_birth):
    today = date.today()
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - date_of_birth.year - ((today.month, today.day) < 
         (date_of_birth.month, date_of_birth.day)) 
  
    return age 