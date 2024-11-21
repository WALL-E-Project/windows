import json
import random
import threading
import cv2
from openai import OpenAI
import speech_recognition as sr
from baseModel import baseModel, send_img_to_gpt, take_photo, send_image_to_LLAVA_server
from function_calling import costum_function
from whisper import whisper_TTS
from conversation_log import log_conversation
from mqtt_client import select_function
import pvporcupine
import pyaudio
import numpy as np
import time
from picamera2 import Picamera2
import RPi.GPIO as GPIO
import threading
# import emotion

r = sr.Recognizer()


while True:
    
    print("Dinliyorum...")
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=3, phrase_time_limit=7)
        text = r.recognize_google(audio, language="tr-TR").lower()
        if not text:
            break
        
        print(text)
        whisper_TTS(filename="response", text=text)

        time.sleep(3)

