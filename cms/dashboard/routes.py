from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from datetime import date, datetime
from cms import db
from cms.models import RecordSchema
from cms.models import MedicalRecord
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from sklearn.cluster import KMeans

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('dashboard.kmeans'))

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
        print(record)
    return jsonify(output)
    return redirect(url_for('patients.index'))

@dashboard.route('/kmeans', methods=['GET'])
def kmeans():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = RecordSchema(many=True, only=['findings', 
        'patient', 'date'])
    output = medical_records_schema.dump(medical_records).data

    clusters = 3

    if(len(output) < clusters):
        data = {'clusters': True}
        return render_template('dashboard/index.html', data=data)
    x = []
    y = []
    dataset = []

    for record in output:
        today = datetime.today()
        temp_date = datetime.strptime(record['date'], '%Y-%m-%dT%H:%M:%S+00:00')
        temp_birth_date = datetime.strptime(record['patient']['date_of_birth'], '%Y-%m-%d')
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
    return render_template('dashboard/index.html', data=data)

def calculate_age(date_of_birth):
    today = date.today()
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - date_of_birth.year - ((today.month, today.day) < 
         (date_of_birth.month, date_of_birth.day)) 
    return age
