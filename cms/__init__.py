from flask import Flask

app = Flask(__name__)

from cms.routes import pages

app.register_blueprint(pages, url_prefix='/')