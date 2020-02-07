from flask import request, make_response, jsonify
from google.cloud import texttospeech
from app import app, speech_client

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
    return response

@app.route("/suggest", methods=["POST"])
def suggest():
    user_word = request.get_json()["user_word"]
    suggested_words = [user_word + str(i) for i in range(3)]
    return jsonify(suggested_words=suggested_words)