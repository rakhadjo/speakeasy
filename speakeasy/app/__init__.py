from flask import Flask
from google.cloud import texttospeech
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
speech_client = texttospeech.TextToSpeechClient()

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="speakeasy"
)

cursor = connection.cursor()


from app import routes, api_routes
