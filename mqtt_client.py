import paho.mqtt.client as paho
from process.process_queue import ProcessQueue
from whisper import whisper_TTS
from conversation_log import get_conversation_log, log_conversation

process_queue = ProcessQueue.get_instance()

# Broker bilgileri
broker_address = "broker.emqx.io"
broker_port = 1883

client = paho.Client()

# MQTT client - Mesaj alma (subscriber) ve publish işlemleri
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {broker_address} with result code {rc}")
        # Abone olunacak konular
        client.subscribe("get_alarm", qos=1)
        client.subscribe("get_reminder", qos=1)
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print("Message published")

def on_message(client, userdata, message):
    print(f"Received message '{message.payload.decode()}' on topic '{message.topic}' with QoS {message.qos}")
    
    payload = message.payload.decode()
    
    if message.topic == "get_alarm":
        print("\nAlarm set mesajı alındı*********")
        process_queue.add_task(whisper_TTS, "response", f"alarm için hatırlatıcı kurmamı istemiştiniz.")

    elif message.topic == "get_reminder":
        print("\nReminder set mesajı alındı*********")
        process_queue.add_task(whisper_TTS, "response", f"{payload} hatırlatmamı istemiştiniz.")
        
    else:
        print("Unknown topic")

def on_disconnect(client, userdata, rc):
    print(f"Disconnected with result code {rc}")

# MQTT bağlantısını başlat
def start_mqtt_client():
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    try:
        client.connect(broker_address, broker_port, keepalive=60)
        client.loop_start()  # Başlat ve döngüye al
    except Exception as e:
        print(f"An error occurred: {e}")

# Mesaj yayınlama fonksiyonu
def publish_message(topic, payload, qos=1):
    result = client.publish(topic, payload=payload, qos=qos)
    
    if result.rc == paho.MQTT_ERR_SUCCESS:
        print("Message published successfully")
    else:
        print(f"Failed to publish message: {result.rc}")

# select function for mqtt client
def select_function(function_name, function_parameters):
    if function_name in ["update_tableLamp_status", "set_reminder", "update_roomLamp_status", "set_alarm"]:
        publish_message(f"{function_name}", f"{function_parameters}", 1)
    else:
        print("Function not found")
        return False
    return True


def start_mqtt():

    # MQTT istemcisini başlat
    start_mqtt_client()

    # MQTT istemcisinin mesaj almak için döngüde kalmasını sağla
    client.loop_forever()