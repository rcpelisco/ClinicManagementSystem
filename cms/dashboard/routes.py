from flask import Blueprint, render_template, url_for, redirect

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/', methods=['GET', 'POST'])
def index():
    return redirect(url_for('patients.index'))
