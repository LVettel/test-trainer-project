from flask import Flask

app = Flask(__name__, instance_relative_config=True, static_url_path='/app', static_folder='static')
#app.config.from_pyfile('config.py')

from app import views

