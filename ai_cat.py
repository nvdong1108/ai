from google.cloud import texttospeech
from flask import Flask, request, jsonify, send_from_directory
import pyttsx3

import os
from gtts import gTTS
import uuid

app = Flask(__name__)

if not os.path.exists('audio'):
    os.makedirs('audio')


def google_cloud_tts(text, gender):
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.SynthesisInput(text=text)

    print(f"{gender}")
    voice = texttospeech.VoiceSelectionParams(
        language_code="vi-VN",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE if gender == "FEMALE" else texttospeech.SsmlVoiceGender.MALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")




def voice_pyttsx3(_lang, text,gender="female"):
    filename = str(uuid.uuid4()) + '.mp3'
    filepath = os.path.join('audio', filename)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if gender == "male":
        engine.setProperty('voice', voices[0].id)
    elif gender == "female":
        engine.setProperty('voice', voices[1].id)
    
    # engine.say(text)
    engine.save_to_file(text, filepath)
    engine.runAndWait()
   
    return filename


def voice_gTTS(_lang, text):
     filename = str(uuid.uuid4()) + '.mp3'
     filepath = os.path.join('audio', filename)
     
     tts = gTTS(text=text, lang=_lang)
     tts.save(filepath)
     return filename


@app.route('/text-to-speech', methods=['POST'])
def text_to_speech_api():
    print(f" body request  {request.get_json}")
    text = request.get_json()['text']
    _lang = request.get_json()['lang']
    lib  = request.get_json()['lib']
    gender  = request.get_json()['gender']
    # en fr es ja ko vn
    # 
    if _lang is None:
        _lang = 'vi'
    print(f'{_lang} ,  {lib} ')

    
    filename = None

    if lib == 'sx3':
        print(f"generate by voice_pyttsx3")
        filename = voice_pyttsx3(_lang, text, gender)
    elif lib == 'g_cloud':
        google_cloud_tts(text, gender)
    else:
        print(f"generate by gtts")
        filename = voice_gTTS(_lang, text)    
    
    
    full_url = request.host_url + 'audio/' + filename
    return jsonify({'url': full_url})




@app.route('/audio/<filename>', methods=['GET'])
def get_audio(filename):
    return send_from_directory('audio', filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=False)