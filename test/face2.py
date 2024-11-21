import time
import RPi.GPIO as GPIO
import cv2
from picamera2 import Picamera2


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)  # Orta pozisyon (90 derece)

servoPosition = 90

RES = (640, 480)
picam2 = Picamera2()
picam2_config = picam2.create_still_configuration(main={"size": RES})
picam2.configure(picam2_config)
picam2.start()

def set_servo_angle(angle):
    duty = 2.5 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)

def find_face_y_coordinate():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = picam2.capture_array()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    if len(faces) > 0:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        center_y_coord = y + h // 2
        return center_y_coord
    
    else:
        print("Yüz tespit edilemedi.")
        return None


# POSITION_THRESHOLD = 20  # Servo motorun hareket etmesi için gereken minimum fark
# SERVO_MOVE_DELAY = 0.5   # Servo motorun hareketleri arasındaki bekleme süresi (saniye)

while True:
    face_y = find_face_y_coordinate()

    if face_y is not None:
        print(f"Yüzün y koordinatı: {face_y}")
        
        # Servo motorun konumu ile yüzün konumu arasındaki fark POSITION_THRESHOLD'dan büyükse servo motorun açısını ayarla
        # if abs(face_y - (RES[1] // 2)) > POSITION_THRESHOLD:
        if face_y < RES[1] // 2:
            print("Yüz ekranın üst yarısında.")
            servoPosition = min(180, servoPosition + 5)
        elif face_y > RES[1] // 2:
            print("Yüz ekranın alt yarısında.")
            servoPosition = max(0, servoPosition - 5)
        
        set_servo_angle(servoPosition)
        # time.sleep(SERVO_MOVE_DELAY)
    else:
        print("Yüz tespit edilemedi.")

    time.sleep(0.1)
