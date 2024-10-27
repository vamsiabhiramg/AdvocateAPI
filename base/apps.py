from django.apps import AppConfig
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)



class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base'
