from flask import Blueprint, render_template
from flask import redirect, url_for, request, jsonify
from datetime import date, datetime
from cms import db
from cms.models import MedicalRecord, Patient
from cms.models import RecordSchema, PatientSchema
from sqlalchemy import text 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from sklearn.cluster import KMeans
import json

dashboard = Blueprint('dashboard', __name__)

def get_statistics(gender):
    sql = text('''SELECT
            `findings`.`findings`,
            COUNT(`findings`.`findings`) as `case_count`
        FROM
            `findings`,
            `medical_records`,
            `patients`
        WHERE
            `medical_records`.`patient_id` = `patients`.`id` AND 
            `medical_records`.`findings_id` = `findings`.`id` AND
            `patients`.`gender` = '{}'
        GROUP BY 
            `findings`.`findings`'''.format(gender))
    result = db.engine.execute(sql)
    return result

def get_pie():
    query = '''SELECT COUNT(findings.findings) as count,
            patients.address
        FROM
            findings,
            medical_records,
            patients
        WHERE
            findings.id = medical_records.findings_id AND
            medical_records.patient_id = patients.id
        GROUP BY patients.address'''
    
    result = db.engine.execute(query)
    return result

def get_area_most():
    query = '''SELECT count, address FROM 
            (SELECT COUNT(findings.findings) as count,patients.address
        FROM
            findings,
            medical_records,
            patients
        WHERE
            findings.id = medical_records.findings_id AND
            medical_records.patient_id = patients.id
        GROUP BY patients.address) as T ORDER BY count DESC'''

    result = db.engine.execute(query)
    
    return result

@dashboard.route('/', methods=['GET', 'POST'])
def index():
    if current_user.position == 'patient':
        return redirect(url_for('front_page.index'))
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = RecordSchema(many=True, only=['findings', 
        'patient', 'date'])
    output = medical_records_schema.dump(medical_records).data
    male_count = Patient.query.filter(Patient.gender == 'male').count()
    female_count = Patient.query.filter(Patient.gender == 'female').count()

    male_result = get_statistics('male')
    female_result = get_statistics('female')
    
    statistics = {'findings': [], 'patient_count': {'male': 0, 'female': 0}}

    for result in male_result:
        statistics['patient_count']['male'] += result.case_count
        statistics['findings'] += [{ 'name' : result.findings, 
            'male_count': result.case_count, 'female_count': 0 }]

    for result in female_result:
        statistics['patient_count']['female'] += result.case_count
        if not any(entry['name'] == 
            result.findings for entry in statistics['findings']):
            statistics['findings'] += [{ 'name' : result.findings, 
                'male_count': 0,  'female_count': result.case_count }]
        for entry in statistics['findings']:
            if(entry['name'] == result.findings):
                entry['female_count'] = result.case_count
                
    print(statistics)
    # return ''
    clusters = 3

    if(len(output) < clusters):
        data = {'clusters': True}
        return render_template('dashboard/index.html', data=data, 
            statistics=statistics)
    x = []
    y = []
    dataset = []

    for record in output:
        today = datetime.today()
        temp_date = datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S+00:00')
        temp_birth_date = datetime.strptime(record['patient']['date_of_birth'], 
            '%Y-%m-%d')
        date = today - temp_date
        birth_date = today - temp_birth_date
        x += [int(birth_date.days)]
        y += [int(date.days)]
        dataset += [[int(birth_date.days),
            int(date.days)]]
            
    X = np.array(dataset)
    kmeans = KMeans(n_clusters=clusters)
    
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_
    data = [[[] for k in range(clusters)],[[] for k in range(clusters)]]
    for i in range(len(X)):
        plt.plot(X[i][0], X[i][1], labels[i], markersize=5)
        data[0][int(labels[i])] += [[
            int(X[i][0]), 
            int(X[i][1])
        ]]
    for i in range(len(centroids)):
        data[1][i] += [[
            int(centroids[i][0]),
            int(centroids[i][1])
        ]]

    pie = { "data": [], "labels": [] }

    for entry in get_pie():
        pie['data'].append(entry['count'])
        pie['labels'].append(entry['address'])

    pie['labels'] = json.dumps(pie['labels'])
    
    return render_template('dashboard/index.html', data=data, 
        statistics=statistics, pie=pie, most=get_area_most())

@dashboard.route('/all', methods=['GET', 'POST'])
def month():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = RecordSchema(many=True, only=['findings', 
        'patient', 'date'])

    output = medical_records_schema.dump(medical_records).data
    for record in output:
        temp_date = datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S+00:00')
        record['date'] = int(datetime.strftime(temp_date, '%Y%m%d%H%M%S'))
        record['id'] = record['findings']['id']
        record['findings'] = record['findings']['findings']
        record['gender'] = 1 if record['patient']['gender'] == 'Male' else 2
        record['age'] = calculate_age(record['patient']['date_of_birth'])
        del(record['patient'])
        
    return jsonify(output)
    return redirect(url_for('patients.index'))

@dashboard.route('/kmeans', methods=['GET'])
def kmeans():
    pass

def calculate_age(date_of_birth):
    today = date.today()
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - date_of_birth.year - ((today.month, today.day) < 
         (date_of_birth.month, date_of_birth.day)) 
    return age
