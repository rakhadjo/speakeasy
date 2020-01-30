from flask import render_template, request, make_response
from google.cloud import texttospeech
from app import app, speech_client

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/keybind")
def keybind():
    return render_template("keybind.html")

@app.route("/design")
def design():
    return render_template("design.html")

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    if "speech_text" in data:
        synthesis_input = texttospeech.types.SynthesisInput(text=data["speech_text"])
    else:
        raise TypeError

    voice = texttospeech.types.VoiceSelectionParams(
        language_code='en-US',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)

    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    
    google_response = speech_client.synthesize_speech(synthesis_input, voice, audio_config)
    response = make_response(google_response.audio_content)
    response.headers['Content-Type'] = 'audio/mp3'
    response.headers['Content-Disposition'] = 'attachment; filename=sound.mp3'
    with open("output.mp3", "wb") as out:
        out.write(google_response.audio_content)
    return response

    