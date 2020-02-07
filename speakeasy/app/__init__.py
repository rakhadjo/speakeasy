from flask import Flask
from google.cloud import texttospeech

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
speech_client = texttospeech.TextToSpeechClient()

from app import routes, api_routes
