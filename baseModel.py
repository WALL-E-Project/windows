# openai gpt model
import base64
import json
import time
import cv2
from openai import OpenAI
from conversation_log import get_conversation_log, log_conversation
import requests
from datetime import datetime

current_date = datetime.now().date().strftime("%Y-%m-%d %H:%M:%S")
client =  OpenAI(api_key="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")
answer = ""

# Base model for voice assistant
def baseModel(costum_function, prompt):
    """
    this function sends the prompt message to the gpt model and returns the response
    parametres:
    - costum_function: function name
    - prompt: prompt message
    - return: response message
    """

    # Get the last 10 conversation logs
    chat_history = get_conversation_log(count=10)
    formatted_chat_history = []
    for entry in chat_history:
        formatted_chat_history.append({"role": "user", "content": entry['user_message']})
        formatted_chat_history.append({"role": "assistant", "content": entry['response_message']})

    # print(formatted_chat_history)
    costum_messages = [
        {
        "role": "system",
        "content": "You are a friendly person. You usually speak in slang. You constantly swear. You always talk in English. "
        + "You will receive the user message after USER: and visual data after VISION: "
        + "Treat the information provided after VISION: as if you're seeing it with your own eyes. "
        + "Only mention what you 'see' when it's necessary for the context or to answer the user's question. "
        + "Don't explicitly state that you're looking at an image or analyzing visual data. "
        + "Always add your emotional state at the end of your answer like this: emotion:happy. "
        + "Emotion options: [normal, happy, angry]"
        + "Today Date: " + current_date
        },
    #  *formatted_chat_history,
        { "role": "user", "content": f"USER: {prompt} VISION: {answer}"}
    ]
    print(costum_messages)
    openai_response = client.chat.completions.create(
        model = 'gpt-4o',
        messages=costum_messages,
        functions=costum_function,
        function_call= 'auto',
    )

    return openai_response



# vision model for voice assistant

def encode_image_to_base64(frame):
    # Resmi base64 formatına encode et
    _, buffer = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    return img_base64


def take_photo():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    #frame = cv2.resize(frame, (640, 480))
    cap.release()
    cv2.destroyAllWindows()
    return frame


def send_img_to_gpt(frame, prompt = "Resimde ne görüyorsun kısaca açıklarmısın?"):
    """
    this function sends the image to the gpt model and returns the response
    parametres: 
    - frame: image
    - prompt: prompt message
    - return: response message 
    """
    
    img_base64 = encode_image_to_base64(frame)
    # Get the last 10 conversation logs
    chat_history = get_conversation_log(count=10)
    formatted_chat_history = []
    for entry in chat_history:
        formatted_chat_history.append({"role": "user", "content": entry['user_message']})
        formatted_chat_history.append({"role": "assistant", "content": entry['response_message']})


    prompt_msg = {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": prompt
        },

        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{img_base64}"
          }
        }
      ]
    }




    # Parameters for API call
    params = {
        "model": "gpt-4o-mini",
        "messages": [*formatted_chat_history, prompt_msg],
        "max_tokens": 100,
    }
    # Make the API call
    result = client.chat.completions.create(**params)
    return result.choices[0].message.content

def process_response(response):
    full_response = ""
    
    # Split the response by newlines
    for line in response.split('\n'):
        try:
            # Parse each line as JSON
            doc = json.loads(line)
            if "response" in doc:
                full_response += doc["response"]
        except json.JSONDecodeError:
            # If JSON is invalid, skip that line
            pass
    
    return full_response

def send_image_to_LLAVA_server(frame):
    global answer

    """
    this function sends the image to the llava model and returns the response
    parametres:
    - frame: image
    - return: response message
    """

    img_base64 = encode_image_to_base64(frame)

    jsonData = {
            "model": "llava",
            "prompt": "what do you see in the image? Describe how human is looking and what is she/he doing. Answer with one or two short sentences at most",
            "images": [img_base64]
        }
    
    #0.0.0.0: port  olarak ortam değişkenlerine ekle. bilgisayarın ip si üzerinden bağlan. 
    # JSON verisini sunucuya gönder
    response = requests.post(
        "http://192.168.1.114:9568/api/generate",
        json=jsonData,
        timeout=20
    )
    
    answer = process_response(response.text)
    print(answer)
    #response = response.json()
    #answer = response.get('answer', '').lower()
    
    # cevabın analiz edilmesi

    """if "laying" in answer:
        print("Yanıt: Adam uzanıyor.")
        return answer
    elif "sitting" in answer:
        print("Yanıt: Adam oturuyor.")
        return answer
    else:
        return False"""
    

def realtimeVideo():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (320, 240))
        cv2.imshow('frame', frame)
        
        #base64_frame = encode_image_to_base64(frame)
        response = send_img_to_gpt(frame)
        print(response)
        time.sleep(5)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    


"""frame = take_photo()
img_context = send_img_to_gpt(frame ,prompt="az önce gösterdiğim resim ile şimdi gösterdiğim resim arasında nasıl bir bağlantı krabilirsin?")
log_conversation("resimde ne görüyorsun", img_context)
print(img_context)"""