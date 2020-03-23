from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from google.cloud import texttospeech
from app.word_suggestion import word_suggestion

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://d44623mw:SpEaKeAsYx4@dbhost.cs.man.ac.uk/2019_comp10120_x4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

speech_client = texttospeech.TextToSpeechClient()
suggester = word_suggestion(filename="1661-0.txt")
suggester.load("keras_next_word_model.h5")

db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"

DEFAULT_KEYBOARDS = {
        "U+263B": ("Hello, my name is", "I can't speak because", "I am using this app to communicate"),
        "U+25F7": ("What time is", "When are we going to", "When is our next class?"),
        "U+1F374": ("What are you eating for lunch?", "When is lunchtime?", "What time shall we meet?")
        }

from app import routes, api_routes, models
