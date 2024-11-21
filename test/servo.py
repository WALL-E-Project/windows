import RPi.GPIO as GPIO
import time

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo motor pini
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)

# PWM başlat
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(2)  # Başlangıç pozisyonu (0 derece)

try:
    while True:
        # 0 derece
        servo.ChangeDutyCycle(2)
        time.sleep(1)
        
        # 90 derece
        servo.ChangeDutyCycle(7)
        time.sleep(1)
        
        # 180 derece
        servo.ChangeDutyCycle(12)
        time.sleep(1)

except KeyboardInterrupt:
    servo.stop()
    GPIO.cleanup()