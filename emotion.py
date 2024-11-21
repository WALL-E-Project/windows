# import threading
# import time
# import random
# import re
# import json
# import board
# import busio
# from PIL import Image, ImageDraw
# import adafruit_ssd1306

# # OLED display size
# SCREEN_WIDTH = 128
# SCREEN_HEIGHT = 64

# # Setup I2C and OLED display
# i2c = busio.I2C(board.SCL, board.SDA)
# oled = adafruit_ssd1306.SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

# # Reference eye dimensions and spacing
# ref_eye_height = 40
# ref_eye_width = 40
# ref_space_between_eye = 10
# ref_corner_radius = 10

# # Current eye states
# left_eye_height = ref_eye_height
# left_eye_width = ref_eye_width
# left_eye_x = 32
# left_eye_y = 32
# right_eye_x = 32 + ref_eye_width + ref_space_between_eye
# right_eye_y = 32
# right_eye_height = ref_eye_height
# right_eye_width = ref_eye_width

# running_saccade = True
# running_chat = True

# globalEmotion = "sleep"
# globalLastEmotion = ""
# globalLastBlinkTime = time.time()
# # Drawing the eyes
# def draw_eyes(update=True):
#     global globalLastEmotion

#     image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
#     draw = ImageDraw.Draw(image)

#     # Draw the left eye
#     x = int(left_eye_x - left_eye_width / 2)
#     y = int(left_eye_y - left_eye_height / 2)
#     draw.rounded_rectangle([x, y, x + left_eye_width, y + left_eye_height], radius=ref_corner_radius, fill=255)

#     # Draw the right eye
#     x = int(right_eye_x - right_eye_width / 2)
#     y = int(right_eye_y - right_eye_height / 2)
#     draw.rounded_rectangle([x, y, x + right_eye_width, y + right_eye_height], radius=ref_corner_radius, fill=255)

#     # Send to display
#     if update:
#         oled.image(image)
#         oled.show()
#     globalLastEmotion = "normal"

# def center_eyes(update=True):
#     global globalLastEmotion
    
#     global left_eye_x, left_eye_y, right_eye_x, right_eye_y
#     left_eye_x = SCREEN_WIDTH // 2 - ref_eye_width // 2 - ref_space_between_eye // 2
#     left_eye_y = SCREEN_HEIGHT // 2
#     right_eye_x = SCREEN_WIDTH // 2 + ref_eye_width // 2 + ref_space_between_eye // 2
#     right_eye_y = SCREEN_HEIGHT // 2
#     draw_eyes(update)
#     globalLastEmotion = "centerEyes"

# def blink(speed=37):
#     global globalLastEmotion
#     global globalLastBlinkTime
#     #globalLastEmotion = "blink"
#     global left_eye_height, right_eye_height
#     #drawEyesAcordingToLastEmotion()

#     # Blink down
#     for _ in range(1):
#         left_eye_height -= speed
#         right_eye_height -= speed
#         drawEyesAcordingToLastEmotion()

#     # Blink up
#     for _ in range(1):
#         left_eye_height += speed
#         right_eye_height += speed
#         drawEyesAcordingToLastEmotion()

#     globalLastBlinkTime = time.time()

# def sleep():
#     global globalLastEmotion, left_eye_height, right_eye_height
    
    
#     # Gözlerin yavaşça kapanması için bir döngü kullanıyoruz
#     for h in range(ref_eye_height, 1, -3):  # ref_eye_height'ten 2'ye kadar, 3'er 3'er azalarak
#         left_eye_height = h
#         right_eye_height = h
#         draw_eyes(True)
#         time.sleep(0.05)  # Her adım arasında kısa bir bekleme
    
#     # Son olarak gözlerin tamamen kapandığından emin oluyoruz
#     left_eye_height = 2
#     right_eye_height = 2
#     draw_eyes(True)
#     globalLastEmotion = "sleep"

# def wakeup():
#     global globalLastEmotion, left_eye_height, right_eye_height, globalEmotion

#     for h in range(0, ref_eye_height + 1, 10):  # Adım boyutunu 5'ten 10'a çıkardık
#         left_eye_height = h
#         right_eye_height = h
#         draw_eyes(True)
#     globalLastEmotion = "wakeup"
#     globalEmotion = "normal"

# def happy_eye():
#     global globalLastEmotion

#     image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
#     draw = ImageDraw.Draw(image)

#     # Draw the left eye base (oval shape as the base for happy eyes)
#     x = int(left_eye_x - left_eye_width / 2)
#     y = int(left_eye_y - left_eye_height / 2)
#     draw.rounded_rectangle([x, y, x + left_eye_width, y + left_eye_height], radius=ref_corner_radius, fill=255)

#     # Draw the right eye base (oval shape as the base for happy eyes)
#     x = int(right_eye_x - right_eye_width / 2)
#     y = int(right_eye_y - right_eye_height / 2)
#     draw.rounded_rectangle([x, y, x + right_eye_width, y + right_eye_height], radius=ref_corner_radius, fill=255)

#     # Now add the happy expression (curved lines for the happy eye)
#     for i in range(2):  # Döngü sayısını 2 olarak tutuyoruz
#         offset = ref_eye_height // 2 - i * 7  # Adım büyüklüğünü 7 yapıyoruz
#         # Left eye (smile effect)
#         draw.polygon([(left_eye_x - ref_eye_width // 2 - 1, left_eye_y + offset),
#                       (left_eye_x + ref_eye_width // 2 + 1, left_eye_y + 5 + offset),
#                       (left_eye_x - ref_eye_width // 2 - 1, left_eye_y + ref_eye_height + offset)], fill=0)
        
#         # Right eye (smile effect)
#         draw.polygon([(right_eye_x + ref_eye_width // 2 + 1, right_eye_y + offset),
#                       (right_eye_x - ref_eye_width // 2 - 1, right_eye_y + 5 + offset),
#                       (right_eye_x + ref_eye_width // 2 + 1, right_eye_y + ref_eye_height + offset)], fill=0)

#         # Display the image on OLED screen
#         oled.image(image)
#         oled.show()

#     globalLastEmotion = "happy"

# def saccade_loop():
#     global running_saccade
#     direction_x_movement_amplitude = 8
#     direction_y_movement_amplitude = 6

#     while running_saccade:
#         direction_x = random.choice([-1, 1])
#         direction_y = random.choice([-1, 1])
#         saccade(direction_x, direction_y)
#         time.sleep(3)

# def saccade(direction_x, direction_y):
#     global globalLastEmotion

#     global left_eye_x, right_eye_x, left_eye_y, right_eye_y, left_eye_height, right_eye_height
#     direction_x_movement_amplitude = 4
#     direction_y_movement_amplitude = 3
#     blink_amplitude = 8


#     # Move the eyes
#     left_eye_x += direction_x_movement_amplitude * direction_x
#     right_eye_x += direction_x_movement_amplitude * direction_x
#     left_eye_y += direction_y_movement_amplitude * direction_y
#     right_eye_y += direction_y_movement_amplitude * direction_y
#     left_eye_height -= blink_amplitude
#     right_eye_height -= blink_amplitude
#     drawEyesAcordingToLastEmotion()


#     time.sleep(1)

#     # Move the eyes back
#     left_eye_x -= direction_x_movement_amplitude * direction_x
#     right_eye_x -= direction_x_movement_amplitude * direction_x
#     left_eye_y -= direction_y_movement_amplitude * direction_y
#     right_eye_y -= direction_y_movement_amplitude * direction_y
#     left_eye_height += blink_amplitude
#     right_eye_height += blink_amplitude
#     drawEyesAcordingToLastEmotion()

# def drawEyesAcordingToLastEmotion():
#     if(globalLastEmotion == "angry"):
#         angry()
#     elif(globalLastEmotion == "happy"):
#         happy_eye()
#     else:
#         draw_eyes()

# def angry(update=True):
#     global globalLastEmotion

#     image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
#     draw = ImageDraw.Draw(image)

#     cut_height = int(left_eye_height * 0.3)
#     # Sol göz için
#     left_x = int(left_eye_x - left_eye_width / 2)
#     left_y = int(left_eye_y - left_eye_height / 2)
    
#     # Gözün üst kısmını düz dikdörtgen olarak çiziyoruz
#     draw.rectangle(
#         [left_x, left_y + cut_height, left_x + left_eye_width, left_y  + left_eye_height / 2],
#         fill=255
#     )
    
#     draw.rounded_rectangle(
#         [left_x, left_y + cut_height, left_x + left_eye_width, left_y + left_eye_height],
#         radius=ref_corner_radius,
#         fill=255
#     )

#     # Sağ göz için aynı işlemi tekrarlıyoruz
#     right_x = int(right_eye_x - right_eye_width / 2)
#     right_y = int(right_eye_y - right_eye_height / 2)
    
#     draw.rectangle(
#         [right_x, right_y + cut_height, right_x + right_eye_width, right_y + right_eye_height / 2],
#         fill=255
#     )
    
#     draw.rounded_rectangle(
#         [right_x, right_y + cut_height, right_x + right_eye_width, right_y + right_eye_height],
#         radius=ref_corner_radius,
#         fill=255
#     )

#     # Ekrana gönder
#     if update:
#         oled.image(image)
#         oled.show()

#     globalLastEmotion = "angry"

# def sad_eye():
#     global globalLastEmotion

#     center_eyes()
#     image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
#     draw = ImageDraw.Draw(image)
#     globalLastEmotion = "sad"

#     # Draw the base eyes
#     x_left = int(left_eye_x - left_eye_width / 2)
#     y_left = int(left_eye_y - left_eye_height / 2)
#     x_right = int(right_eye_x - right_eye_width / 2)
#     y_right = int(right_eye_y - right_eye_height / 2)
    
#     draw.rounded_rectangle([x_left, y_left, x_left + left_eye_width, y_left + left_eye_height], radius=ref_corner_radius, fill=255)
#     draw.rounded_rectangle([x_right, y_right, x_right + right_eye_width, y_right + right_eye_height], radius=ref_corner_radius, fill=255)
    
#     # Draw sad eyebrows
#     eyebrow_length = ref_eye_width - 10
#     eyebrow_thickness = 5
    
#     # Left eyebrow
#     draw.polygon([
#         (left_eye_x - eyebrow_length//2, left_eye_y - ref_eye_height//2 + 5),
#         (left_eye_x + eyebrow_length//2, left_eye_y - ref_eye_height//2 - 5),
#         (left_eye_x + eyebrow_length//2, left_eye_y - ref_eye_height//2 - 5 + eyebrow_thickness),
#         (left_eye_x - eyebrow_length//2, left_eye_y - ref_eye_height//2 + 5 + eyebrow_thickness)
#     ], fill=0)
    
#     # Right eyebrow
#     draw.polygon([
#         (right_eye_x - eyebrow_length//2, right_eye_y - ref_eye_height//2 - 5),
#         (right_eye_x + eyebrow_length//2, right_eye_y - ref_eye_height//2 + 5),
#         (right_eye_x + eyebrow_length//2, right_eye_y - ref_eye_height//2 + 5 + eyebrow_thickness),
#         (right_eye_x - eyebrow_length//2, right_eye_y - ref_eye_height//2 - 5 + eyebrow_thickness)
#     ], fill=0)

#     oled.image(image)
#     oled.show()
    

# def runEmotions():
#     global globalEmotion
#     print("Run Emotions içerisinde")
#     while True:
#         randomNum = random.randint(0, 1)
#         #print(globalEmotion)
#         if(globalEmotion =="happy" and globalLastEmotion != "happy"):
#             happy_eye()
#         elif(globalEmotion == "happy" and globalLastEmotion == "happy" and (time.time() - globalLastBlinkTime) > 3):
#             if(randomNum == 0):
#                 blink()
#             else:
#                 direction_x = random.choice([-1, 1])
#                 direction_y = random.choice([-1, 1])
#                 saccade(direction_x, direction_y)

#         if(globalEmotion == "normal"  and globalLastEmotion != "normal"):
#             draw_eyes()
#         elif(globalEmotion == "normal" and globalLastEmotion == "normal" and (time.time() - globalLastBlinkTime) > 3):
            
#             if(randomNum == 0):
#                 blink()
#             else:
#                 direction_x = random.choice([-1, 1])
#                 direction_y = random.choice([-1, 1])
#                 saccade(direction_x, direction_y)


#         if(globalEmotion == "saccade"):
#             direction_x = random.choice([-1, 1])
#             direction_y = random.choice([-1, 1])
#             saccade(direction_x, direction_y)
#         if(globalEmotion == "angry" and globalLastEmotion != "angry"):
#             angry()
#         elif(globalEmotion == "angry" and globalLastEmotion == "angry" and (time.time() - globalLastBlinkTime) > 3):
#             blink()
#         if(globalEmotion == "sad"  and globalLastEmotion != "sad"):
#             sad_eye()
#         if(globalEmotion == "wakeup"  and globalLastEmotion != "sad"):
#             wakeup()

#         if(globalEmotion == "sleep"  and globalLastEmotion != "sleep"):
#             sleep()


# # Start the saccade thread
# def start_emotion_thread():
#     print("Start emotion içerisinde")
#     emotion_thread = threading.Thread(target=runEmotions)
#     emotion_thread.start()
#     print("start emotion bitti")

# def extract_emotion(text):
#     match = re.search(r'emotion:\s*(\w+)', text)
#     if match:
#         return match.group(1)
#     return None





# # def chat(costum_messagess):
# #     global globalEmotion

# #     if openai_response.choices[0].message.function_call:
# #         response = openai_response.choices[0].message.content # burası null dönüyor
# #         function_calling = openai_response.choices[0].message.function_call
# #         function_name = openai_response.choices[0].message.function_call.name
        
# #         # JSON verisini düzenli ve okunabilir hale getiriyoruz
# #         function_parameters_dict = openai_response.choices[0].message.function_call.arguments
# #         function_parameters = json.loads(function_parameters_dict)

# #         print("FONKSİYON ÇALIŞTIRDI")
# #         print("Response: ", response)
# #         # if response:
# #           # emotion = extract_emotion(str(response))
# #           # print("Emotion: ", str(emotion))
# #           # run_emotion(emotion)
# #         # print("Function: ", str(function_calling))
# #         print("Function Parameters: ", (function_parameters_dict))
# #         print("Function Name: " + function_name)
# #         function_parameters = json.loads(function_parameters_dict)

# #         # robotMovement = ""
# #         # # if("angle" in function_parameters and "direction" in  function_parameters):
# #         # #   robotMovement = " You turned to " + str(function_parameters["direction"]) + " with " + str(function_parameters["angle"]) + " angle to find me"
        
# #         robotAnswer = ""
# #         if("answer" in function_parameters):
# #           robotAnswer = function_parameters["answer"]
        
# #         if(robotAnswer != ""):        
# #           costum_messages.append({ "role": "assistant", "content": str(robotAnswer)})
# #         else:
# #           costum_messages.append({ "role": "assistant", "content": "Tamamdır."})

        
# #         # if(robotMovement != ""):        
# #         #   costum_messages.append({ "role": "user", "content": str(robotMovement)})


# #         if function_name == "rotate_camera":
# #             print("rotate_camera")
# #             #whisper_TTS(function_name, function_parameters["confirm_msg"])
# #             #publish_message(f"{function_name}", f"{function_parameters_dict}", 1)

# #         if function_name == "look_user":
# #             print("look_user")


# #     else:
# #         print("SADECE YANIT VERDİ")

# #         if openai_response.choices[0].message.content:
# #           emotion = extract_emotion(str(openai_response.choices[0].message.content))
# #           print("Emotion: ", str(emotion))
# #           globalEmotion = emotion

# #         while True:
# #             if(globalEmotion == globalLastEmotion):
# #                 print("Emotion Bekleniyor.")  
# #                 break

# #         print("Response:", openai_response.choices[0].message.content)
# #         print("Function: None")
# #         costum_messages.append({ "role": "assistant", "content": str(openai_response.choices[0].message.content)})


# # start_emotion_thread()
# # globalEmotion = "wakeup"

# # globalEmotion = "wakeup"



# # while True:
#     # while True:
#     #     if(globalEmotion == globalLastEmotion):
#     #         print("Emotion Bekleniyor.")  
#     #         break
#     # chat(costum_messages)
#     # userInput = input("Konuş: ")
#     # costum_messages.append({"role": "user", "content": userInput})