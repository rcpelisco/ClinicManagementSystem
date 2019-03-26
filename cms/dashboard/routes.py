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

@dashboard.route('/sklearn', methods=['GET'])
def sklearn():
    medical_records = MedicalRecord.query.all()    
    medical_records_schema = RecordSchema(many=True, only=['findings', 'patient'])
    output = medical_records_schema.dump(medical_records).data

    age = []
    gender = []
    dataset = []

    for record in output:
        age += [calculate_age(record['patient']['date_of_birth'])]
        gender += [1 if record['patient']['gender'] == 'Male' else 2]
        dataset += [[calculate_age(record['patient']['date_of_birth']), 
            1 if record['patient']['gender'] == 'Male' else 2]]

    plt.scatter(age, gender)
    plt.show()

    X = np.array(dataset)
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(X)

    centroids = kmeans.cluster_centers_
    labels = kmeans.labels_

    print(centroids)
    print(labels)

    colors = ['g.', 'r.', 'b.']

    for i in range(len(X)):
        print('Coordinate:', X[i][0], X[i][1], ', Label:', labels[i])
        plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize=10)

    plt.scatter(centroids[:, 0], centroids[:, 1], marker='x', s=150, linewidths=5, zorder=10)
    plt.show()
    return jsonify(dataset)

def calculate_age(date_of_birth):
    today = date.today()
    date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    age = today.year - date_of_birth.year - ((today.month, today.day) < 
         (date_of_birth.month, date_of_birth.day)) 
    return age
