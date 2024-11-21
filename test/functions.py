from openai import OpenAI
import json
from mqtt_client import publish_message
from function_calling import costum_function
from whisper import whisper_TTS, whisper_STT
import random
from baseModel import baseModel

client = OpenAI()

prompt_2 = "masa lambasını açar mısın bebeğim?"
prompt_3 = "çarşamba saat 20:00'da bilal ile toplantım var. Bu çok önemli!"
prompt_5 = "odanın lambasını kapatsana uykum geldi"
prompt_6 = "yarın sabah gibi spora gitmem lazım."
prompt_7 = "yarın saat 10:00'da beni uyandır."

name = ["hasan berat","canım","bitanem","sevgilim"]
selected_name = random.choice(name)

prompts = [ prompt_2, prompt_3, prompt_5, prompt_6, prompt_7]

for prompt in prompts:
    openai_response = baseModel(costum_function, prompt)
    
    if openai_response.choices[0].message.function_call:
        response = openai_response.choices[0].message.content # burası null dönüyor
        function_calling = openai_response.choices[0].message.function_call
        function_name = openai_response.choices[0].message.function_call.name
        
        # JSON verisini düzenli ve okunabilir hale getiriyoruz
        function_parameters_dict = openai_response.choices[0].message.function_call.arguments
        function_parameters = json.loads(function_parameters_dict)

        print("************************************")
        print("Prompt: ", prompt)
        print("Response: ", response)
        print("Function: ", function_calling)
        print("Function Parameters: ", (function_parameters_dict))

        # depending function calling connetion mqtt server.
        if function_name == "update_tableLamp_status":
            whisper_TTS(function_name, function_parameters["confirm_msg"])
            publish_message(f"{function_name}", f"{function_parameters_dict}", 1)
                
        elif function_name == "set_reminder":
            whisper_TTS(function_name, function_parameters["confirm_msg"])
            publish_message(f"{function_name}", f"{function_parameters_dict}", 1)

        elif function_name == "update_roomLamp_status":
            whisper_TTS(function_name, function_parameters["confirm_msg"])
            publish_message(f"{function_name}", f"{function_parameters_dict}", 1)

        elif function_name == "set_alarm":
            whisper_TTS(function_name, function_parameters["confirm_msg"])
            publish_message(f"{function_name}", f"{function_parameters_dict}", 1)
        

    else:
        print("************************************")
        print(prompt)
        print("Response:", openai_response.choices[0].message.content)
        print("Function: None")



