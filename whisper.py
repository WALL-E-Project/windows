import time
import numpy as np
from openai import OpenAI
import warnings
import pyaudio  
import wave 
import whisper  # Add this line to import the whisper module
import io
import os
# import emotion


# OpenAI API client
client = OpenAI(api_key="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")
warnings.filterwarnings("ignore", category=DeprecationWarning)

def whisper_TTS(filename: str, text: str):
    speech_file_path =f"speak/{filename}.wav"
    response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input= text,
    response_format="wav"
    )
    try:
        response.stream_to_file(speech_file_path)
    except Exception as e:
        print(f"Error: {e}")

    # emotion.globalEmotion = emotion.extract_emotion(text)
    # print("Global Emotion:", emotion.globalEmotion)
    #play audio
    print("Ses dosyası çalınıyor...")
    
    #define stream chunk   
    chunk = 1024  
    
    #open a wav format music  
    f = wave.open(speech_file_path,"rb")  
    #instantiate PyAudio  
    p = pyaudio.PyAudio()  
    #open stream  
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                    channels = f.getnchannels(),  
                    rate = f.getframerate(),  
                    output = True)  
    #read data  
    data = f.readframes(chunk)  
    
    #play stream  
    while data:  
        stream.write(data)  
        data = f.readframes(chunk)  
    
    #stop stream  
    stream.stop_stream()  
    stream.close()  
    
    #close PyAudio  
    p.terminate() 


# Transcribe audio
def whisper_STT(filename: str):
    audio_file = open(f"{filename}", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        prompt="",
        language="tr"
    )

    transcription_text = transcription.text
    return transcription_text



"""
# Whisper modelini yükleyin
model = whisper.load_model("base")  # "small", "medium", "large" gibi farklı boyutlarda modelleri kullanabilirsiniz

# PyAudio ayarları
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # Sessizlik eşiği

p = pyaudio.PyAudio()

def listen_and_respond(model, silence_duration=5):
    """"""
    Kullanıcının konuşmasını dinler, konuşma bittikten sonra 5 saniye daha dinlemeye devam eder,
    Whisper ile metne çevirir ve OpenAI API'sine gönderir.
    
    Parameters:
        whisper_model: whisper.Model object
            Whisper model instance to use for transcription.
        silence_duration: int
            The duration in seconds to wait after the user stops talking before ending the recording.
    """"""
    print("Listening...")

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    silent_chunks = 0
    started_talking = False

    while True:
        data = stream.read(CHUNK)
        frames.append(data)
        audio_level = max(data)

        if audio_level > THRESHOLD:
            started_talking = True
            silent_chunks = 0  # Sıfırla çünkü kullanıcı konuşuyor
        else:
            if started_talking:
                silent_chunks += 1

        # Eğer kullanıcı konuşmayı bırakmış ve belirtilen süre geçmişse kaydı durdur
        if silent_chunks > int(RATE / CHUNK * silence_duration):
            print("Recording stopped.")
            break

    # Ses dosyasını kaydet
    wf = wave.open("output.wav", 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Whisper ile metne dönüştür
    result = model.transcribe("output.wav")
    text = result["text"]
    print(f"You said: {text}")

    if not text:
        print("No speech detected.")
        return None
    else:
        return text
"""


def record_audio(filename="speak/recorded_audio.wav", silence_threshold=750, silence_duration=2):
    format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    audio_interface = pyaudio.PyAudio()

    stream = audio_interface.open(format=format, channels=channels,
                                  rate=rate, input=True,
                                  frames_per_buffer=chunk)

    print("Ses kaydediliyor...")
    frames = []
    silence_start_time = None

    for _ in range(0, int(rate / chunk * 60)):  # Max 60 seconds
        data = stream.read(chunk)
        frames.append(data)
        
        audio_data = np.frombuffer(data, dtype=np.int16)
        audio_level = np.abs(audio_data).mean()
        print(f"Amplitude Level: {audio_level}")

        if audio_level < silence_threshold:
            if silence_start_time is None:
                silence_start_time = time.time()
            elif time.time() - silence_start_time >= silence_duration:
                print("Sessizlik tespit edildi. Kaydı durdurma işlemi başlatılıyor.")
                break
        else:
            silence_start_time = None

    print("Ses kaydı tamamlandı ve kaydediliyor.")

    stream.stop_stream()
    stream.close()
    audio_interface.terminate()

    # Eğer hiç ses kaydedilmemişse, dosyayı sil ve False döndür
    if len(frames) == 0:
        print("Hiç ses kaydedilmedi. False döndürülüyor.")
        if os.path.exists(filename):
            os.remove(filename)
        return False

    # Ses kaydını dosyaya yaz
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(audio_interface.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Ses dosyası '{filename}' olarak kaydedildi.")
    return True