from flask import Flask
from google.cloud import texttospeech

app = Flask(__name__)
speech_client = texttospeech.TextToSpeechClient()

from app import routes
