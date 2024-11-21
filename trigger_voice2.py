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
from motor import handleMovementResponse

# from picamera2 import Picamera2
# import RPi.GPIO as GPIO
import threading
# import emotion
from process.process_queue import ProcessQueue
from controlServo import control_servo


process_queue = ProcessQueue.get_instance()
process_size = process_queue.size()
name = "Hasan Berat"
greetings = [
    f"Nasılsın {name} nasıl gidiyor?",
    f"Sana nasıl yardımcı olabilirim {name}?",
    f"Selam, sana nasıl yardımcı olabilirim bugün?"
            ]
access_key = "hxWzHllCuQXMQgvgHWt10UvJgJGeTQjzDvedrBetJqfVY4WYxZwK5A=="  # Buraya kendi erişim anahtarınızı yazın
# peraltaPath = "Peralta_en_raspberry-pi_v3_0_0.ppn"  # Dosya yolunu burada belirtin

porcupine = pvporcupine.create(
    access_key=access_key,  # Erişim anahtarını doğrudan kullanın
    # keyword_paths=[peraltaPath]  # keyword_paths listesi içinde tanımlayın
    keywords=['bumblebee']

)

r = sr.Recognizer()
emotionFlag = False

pa = pyaudio.PyAudio()
audio_stream = pa.open(rate=porcupine.sample_rate, 
                       channels=1, 
                       format=pyaudio.paInt16, 
                       input=True, 
                       frames_per_buffer=porcupine.frame_length)


def listen_wake_word():
    global emotionFlag
    while True:

        if process_queue.is_empty()  == False:
            process_queue.execute_all()
            #print("Queue ya girdi.")
        
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = np.frombuffer(pcm, dtype=np.int16)
        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Wake word detected.")
            listen_and_response()

    
"""
this function listens to the user and responds to the user
"""
def listen_and_response():
    global emotionFlag
    if emotionFlag != True:
        emotionFlag = True
        text = "wakeup"
        # emotion.globalEmotion = text
    while True:
        try:
            with sr.Microphone() as source:
                print("Dinliyorum...")
                audio = r.listen(source, timeout=3, phrase_time_limit=7)
                text = r.recognize_google(audio, language="tr-TR").lower()
                print("--------text: ", text)
                if not text:
                    break
                # elif "baksana" in text:
                #     prompt = text
                #     print("Prompt: ", prompt)
                #     frame = take_photo()
                #     img_context = send_img_to_gpt(frame, prompt)
                #     whisper_TTS("response", img_context)
                #     log_conversation(prompt, img_context)
                #     listen_and_response(source)
                else:
                    response = baseModel(costum_function=costum_function, prompt=text)
                    function_calling = response.choices[0].message.function_call
                    
                    if function_calling:
                        response_text = json.loads(response.choices[0].message.function_call.arguments)["confirm_msg"]
                        print(response_text)
                        
                        # newEmotion = emotion.extract_emotion(response_text)
                        # if(newEmotion != None):
                        #     emotion.globalEmotion = newEmotion
                        #     print("Global Emotion:", emotion.globalEmotion)
                        #     response_text = response_text.replace("emotion: "+emotion.globalEmotion, "")
                        #     response_text = response_text.replace("emotion:"+emotion.globalEmotion, "")
                        
                        function_name = response.choices[0].message.function_call.name
                        if(function_name == "control_movement"):
                            handleMovementResponse(response.choices[0].message.function_call.arguments)
                        
                        if function_name == "control_head_movement":
                            # Parse servo command from arguments
                            servo_args = json.loads(response.choices[0].message.function_call.arguments)
                            control_servo(servo_args["status"])  # Pass up/down command to servo control
                            print("--------servo command: ", servo_args["status"])
                        else:
                            # mqtt send message for other functions
                            thread = threading.Thread(
                                target=select_function,
                                args=(function_name, response.choices[0].message.function_call.arguments)
                            )       
                            thread.start()
                    else:
                        response_text = response.choices[0].message.content
                        print(response_text)
                        # newEmotion = emotion.extract_emotion(response_text)
                        # if(newEmotion != None):
                        #     emotion.globalEmotion = emotion.extract_emotion(response_text)
                        #     print("Global Emotion:", emotion.globalEmotion)
                        #     response_text = response_text.replace("emotion: "+emotion.globalEmotion, "")
                        #     response_text = response_text.replace("emotion:"+emotion.globalEmotion, "")

                    whisper_TTS(filename="response", text=response_text)
                    log_conversation(text, response_text)
                    #listen_and_response(source)
                    #break
                
        except sr.WaitTimeoutError:
            print("WaitTimeoutError")
            # listen_wake_word(source)
            emotionFlag = False
            # emotion.globalEmotion = "sleep"
            break

        except sr.RequestError as e:
            print("Request Error: ", e)
            # listen_wake_word(source)
            emotionFlag = False
            # emotion.globalEmotion = "sleep"
            break

        except sr.UnknownValueError:
            print("UnknownValueError")
            # listen_wake_word(source)
            emotionFlag = False
            # emotion.globalEmotion = "sleep"
            break


# def llava_analyze():
#     # todo: saat başı soracak
#     picam2 = Picamera2()
#     camera_info = picam2.global_camera_info()
#     # print("cameras")
#     # print("cameras : "+camera_info)
    
    
#     config = picam2.create_preview_configuration(main={"format": 'RGB888'})
#     picam2.configure(config)
#     picam2.start()
    
#     time.sleep(2)  # Kameranın başlaması için kısa bir bekleme

#     # cap = cv2.VideoCapture(0)
#     while True:
#         time.sleep(0.1)  # CPU'yu yormamak için kısa bir bekleme
#         # Kameradan görüntü al
#         frame = picam2.capture_array()

#         # Görüntüyü gri tonlamaya çevir
#         # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         # ret, frame = cap.read()
#         # if not ret:
#         #     print("GEldim Buraya2")
#         #     break
        
#         send_image_to_LLAVA_server(frame)
#         #baseModel.answer
        
        """if action:
                if "the man is laying" in action:
                    whisper_TTS("response", "oda lambasını kapatmamı istermisiniz?")
                    log_conversation(" ", "oda lambasını kapatmamı istermisiniz?")
                    listen_and_response(source)
                    break

                if  "the man is sitting" in action:
                    # todo: postür kontrolü yapılması gerekiyor
                    prompt = "Resimde oturan kişinin postürünü değerlendir. Kişi dik mi oturuyor yoksa kambur mu duruyor? Eğer kambur duruyorsa, onu uyar!. Tavsiye vermeni istemiyorum."
                    return_msg = send_img_to_gpt(frame, prompt)
                    whisper_TTS("response", return_msg)
                    log_conversation("şu anda oturuyorum postürümü kontrol edermsini?", f"tabii ki kontrol edebilirim. {return_msg}")
                    break"""
