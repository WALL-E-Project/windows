"""
record audio
text to speech fonksiyonu
speech to text fonksiyonu

"""
import os
from openai import OpenAI
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
from gtts import gTTS
import random
from baseModel import baseModel
from function_calling import costum_function


from whisper import whisper_TTS, whisper_STT, record_audio

language = "tr-TR"
client = OpenAI()

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init("dummy")
voice = engine.getProperty('voices')[1]
engine.setProperty('voice', voice.id)

name = "Hasan Berat"
greetings = [f"Nasılsın {name} nasıl gidiyor?",
             f"Sana nasıl yardımcı olabilirim {name}?",
             f"merhaba canım, sana nasıl yardımcı olabilirim?",]

greeting = random.choice(greetings)


def listen_for_wake_word(source):
    print("Listening for 'selam'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="tr-TR")
            print(text)
            if "selam" in text.lower():
                print("Wake word detected.")
                whisper_TTS(filename="greeting.mp3", text=greeting)
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass


def listen_and_respond(source):
    print("Listening...")
    while True:
        record_audio()
        try:
            
            text = whisper_STT("speak/recorded_audio.wav")
            response = baseModel(costum_function=costum_function, prompt=text)
            response_text = response.choices[0].message.content            
            whisper_TTS(filename="response.mp3", text=response_text)
            
            print("speaking...")
            if not text:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            print("Silence detected, returning to wake word listening...")
            listen_for_wake_word(source)
            break
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
