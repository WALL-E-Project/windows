import json
import speech_recognition as sr
from datetime import datetime

def log_conversation(user_message, response_message, file_name='logs/conversation_log.json'):
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'user_message': user_message,
        'response_message': response_message
    }
    try:
        # Dosya mevcut değilse, oluşturulacak
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        except json.JSONDecodeError:
            data = []
        
        data.append(log_entry)
        
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


# istenilen sayıda güncel konuşma kaydını jsondan okur ve listeye cevirir. 
def get_conversation_log(file_name='logs/conversation_log.json', count=10):
    try:
        with open(file_name, 'r') as file:
            data = json.load(file)
            return data[-count:]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception as e:
        print(f"Bir hata oluştu: {e}")
        return []
    
# log_conversation("ben hasan berat", "merhaba, hasan berat?")
# log_conversation("ben başaşkşehirde oturuyorum", "tamam napim?")
# log_conversation("seni kim tasarladı?", "beni bilal ve hasan berat adlı iki dahi mühendis tasarladı.")
