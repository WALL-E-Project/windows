
import threading
import speech_recognition as sr
from trigger_voice2 import listen_wake_word #, llava_analyze
# from trigger_voice2 import llava_analyze
# from mqtt_client import subscribe_to_topic
# from emotion import runEmotions
from baseModel import realtimeVideo
from mqtt_client import start_mqtt

threads = []

def run_threads():

    try:
        #llava_analyze()
        #listen_wake_word()
        # # Dinleme ve analiz işlemlerini eş zamanlı başlat
        thread1 = threading.Thread(target=listen_wake_word)
        #thread4 = threading.Thread(target=runEmotions)
        #thread2 = threading.Thread(target=llava_analyze)
        # #thread2 = threading.Thread(target=realtimeVideo)
        #thread3 = threading.Thread(target=start_mqtt)
        
        threads.extend([thread1])  # Thread'leri listeye ekle
        # threads.extend([thread1, thread3])
        thread1.start()
        #thread2.start()
        # thread3.start()
        # thread3.start()
        # thread4.start()

        for t in threads:
            t.join()

    except KeyboardInterrupt:
        print("Program kapatılıyor...")
        for t in threads:
            if t.is_alive():
                t.join(timeout=1)  # Timeout ile bekle, sonra zorla durdur

        print("Tüm thread'ler durduruldu.")

if __name__ == "__main__":
    run_threads()