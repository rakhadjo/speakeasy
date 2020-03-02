from flask import request, make_response, jsonify
from google.cloud import texttospeech
from flask_login import current_user
from app import app, speech_client, db
from app.db_functions import update_keyboards_db
from app.models import User

@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    if "speech_text" in data:
        synthesis_input = texttospeech.types.SynthesisInput(text=data["speech_text"])
    else:
        raise TypeError #is that a good idea?
    genders = {
            "MALE": texttospeech.enums.SsmlVoiceGender.MALE,
            "NEUTRAL": texttospeech.enums.SsmlVoiceGender.NEUTRAL,
            "FEMALE": texttospeech.enums.SsmlVoiceGender.FEMALE
            }
    if current_user.is_authenticated:
        u = User.query.filter_by(id=current_user.id).first()
        language_code = u.accent
        ssml_gender = genders[u.gender]
    else:
        language_code = "en-US"
        ssml_gender = texttospeech.enums.SsmlVoiceGender.NEUTRAL

    voice = texttospeech.types.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender)

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

@app.route("/updateKeyboards", methods=["POST"])
def update_keyboards():
    data = request.get_json()
    keyboards = dict()
    for keyboard in data:
        if not clean_keyboard(keyboard):
            return jsonify(False)
        icon, phrases = keyboard
        keyboards[icon] = phrases
    update_keyboards_db(keyboards)
    return jsonify(True)

def clean_keyboard(keyboard):
    if isinstance(keyboard, list) and len(keyboard) != 2:
        return False
    else:
        return False
    icon, phrases = keyboard
    if isinstance(icon, str) and len(icon) > 2:
        try:
            chr(int(icon[2:], 16)) #Tries to convert hex value into unicode char
        except ValueError:
            return False
    else:
        return False
    if isinstance(phrases, list):
        if len(phrases) != 3 or not all(isinstance(phrase, str) for phrase in phrases):
            return False
    else:
        return False
    return True
