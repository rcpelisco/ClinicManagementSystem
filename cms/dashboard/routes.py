from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from cms import db
from cms.models import MedicalRecordSchema
from cms.models import MedicalRecord

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('patients.index'))

@dashboard.route('/month', methods=['GET', 'POST'])
def month():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = MedicalRecordSchema(many=True)
    output = medical_records_schema.dump(medical_records).data
    return jsonify(output)
    return redirect(url_for('patients.index'))
