# import RPi.GPIO as GPIO
from time import sleep
import json

# # GPIO pinleri tanımlayın
# Motor1_IN1 = 17
# Motor1_IN2 = 27
# Motor1_ENA = 18

# Motor2_IN3 = 22
# Motor2_IN4 = 23
# Motor2_ENB = 13

# # GPIO modunu ayarla
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(Motor1_IN1, GPIO.OUT)
# GPIO.setup(Motor1_IN2, GPIO.OUT)
# GPIO.setup(Motor1_ENA, GPIO.OUT)
# GPIO.setup(Motor2_IN3, GPIO.OUT)
# GPIO.setup(Motor2_IN4, GPIO.OUT)
# GPIO.setup(Motor2_ENB, GPIO.OUT)

# # PWM başlat
# pwm1 = GPIO.PWM(Motor1_ENA, 100)  # Motor 1 için PWM
# pwm2 = GPIO.PWM(Motor2_ENB, 100)  # Motor 2 için PWM
# pwm1.start(0)
# pwm2.start(0)

def handleMovementResponse(parameters):

    parameters_str = json.dumps(parameters)
    print(f"Parameters received: {parameters_str}")

    if "turn_left" in parameters:
        print("Turning left")
        # Add your code here for turning left
    elif "turn_right" in parameters :
        print("Turning right")
        # Add your code here for turning right
    elif "forward" in parameters:
        print("Moving forward")
        # Add your code here for moving forward
    elif "backward" in parameters:
        print("Moving backward")
        # Add your code here for moving backward"
    #find true parameter
    # if("turn_left" in parameters):
    #     motor1_forward()
    #     sleep(2)
    #     stop_motors()
    # elif("turn_right" in parameters):
    #     motor2_forward()
    #     sleep(2)
    #     stop_motors()
    # elif("forward" in parameters):
    #     motor1_forward()
    #     motor2_forward()
    #     sleep(2)
    #     stop_motors()
    # elif("backward" in parameters):
    #     motor1_backward()
    #     motor2_backward()
    #     sleep(2)
    #     stop_motors()


# Motor kontrol fonksiyonları
def motor1_forward(speed = 50):
    print("Motor 1 ileri hareket ettiriliyor.")
    # GPIO.output(Motor1_IN1, GPIO.HIGH)
    # GPIO.output(Motor1_IN2, GPIO.LOW)
    # pwm1.ChangeDutyCycle(speed)

def motor1_backward(speed  = 50):
    print("Motor 1 geri hareket ettiriliyor.")
    # GPIO.output(Motor1_IN1, GPIO.LOW)
    # GPIO.output(Motor1_IN2, GPIO.HIGH)
    # pwm1.ChangeDutyCycle(speed)

def motor2_forward(speed = 50):
    print("Motor 2 ileri hareket ettiriliyor.")
    # GPIO.output(Motor2_IN3, GPIO.HIGH)
    # GPIO.output(Motor2_IN4, GPIO.LOW)
    # pwm2.ChangeDutyCycle(speed)

def motor2_backward(speed = 50):
    print("Motor 2 geri hareket ettiriliyor.")
    # GPIO.output(Motor2_IN3, GPIO.LOW)
    # GPIO.output(Motor2_IN4, GPIO.HIGH)
    # pwm2.ChangeDutyCycle(speed)

def stop_motors():
    print("Tüm motorlar durduruluyor.")
    # GPIO.output(Motor1_IN1, GPIO.LOW)
    # GPIO.output(Motor1_IN2, GPIO.LOW)
    # GPIO.output(Motor2_IN3, GPIO.LOW)
    # GPIO.output(Motor2_IN4, GPIO.LOW)
    # pwm1.ChangeDutyCycle(0)
    # pwm2.ChangeDutyCycle(0)

