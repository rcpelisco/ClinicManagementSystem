from flask import Blueprint, render_template

pages = Blueprint('pages', __name__)

@pages.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@pages.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@pages.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')