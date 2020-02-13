from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from google.cloud import texttospeech

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:password@localhost/speakeasy"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
speech_client = texttospeech.TextToSpeechClient()

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"

DEFAULT_KEYBOARDS = {
        "U+0FCA": ("Hello world", "This is a test", "test test"),
        "U+231A": ("blablabla", "hihihi", "huhuhuhuh"),
        "U+2328": ("zaxzaz", "blop blop", "jujujuju")
        }

from app import routes, api_routes, models
