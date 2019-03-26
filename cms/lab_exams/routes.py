from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from cms import db
from datetime import datetime
from flask_login import current_user
from cms.models import LabExam
from cms.lab_exams.forms import CreateCBCExamForm, EditCBCExamForm
from cms.lab_exams.forms import CreateLabExamForm, EditLabExamForm

lab_exams = Blueprint('lab_exams', __name__)

@lab_exams.route('/', methods=['GET'])
def index():
    lab_exams = LabExam.query.all()
    return ''