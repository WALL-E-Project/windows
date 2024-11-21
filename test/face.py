import cv2
import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
import threading

# GPIO ayarları
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo motor pini (GPIO 12)
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Global değişkenler
current_angle = 90
servo_lock = threading.Lock()

def set_servo_angle(angle):
    """Servo motoru belirtilen açıda döndür ve PWM'i kapat."""
    duty = 2.5 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.5)  # Hareketin tamamlanması için bekleme
    servo.stop()  # Servo titremesini önlemek için PWM'i kapat
    global current_angle
    current_angle = angle  # Mevcut açıyı güncelle

def move_servo(target_angle):
    """Servo motorun yavaşça hareket etmesi için ayrı bir thread."""
    global current_angle
    with servo_lock:
        print("lock içinde current angle: " + str(current_angle) + " target angle: " + str(target_angle))
        if current_angle != target_angle:
            servo.start(0)  # Servo motoru başlat
            if current_angle < target_angle:
                current_angle = min(current_angle + 15, target_angle)
            elif current_angle > target_angle:
                current_angle = max(current_angle - 15, target_angle)
            set_servo_angle(current_angle)
            servo.stop()  # Titremeyi önlemek için durdur
        time.sleep(0.2)

def face_recognition():
    global current_angle

    # Yüz algılama için Haarcascade modelini yükle
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    # Picamera2 kullanarak kamera başlat
    picam2 = Picamera2()
    config = picam2.create_preview_configuration(main={"format": 'RGB888'})
    picam2.configure(config)
    picam2.start()

    time.sleep(2)  # Kameranın başlaması için kısa bir bekleme

    while True:
        time.sleep(0.1)  # CPU'yu yormamak için kısa bir bekleme
        # Kameradan görüntü al
        frame = picam2.capture_array()

        # Görüntüyü gri tonlamaya çevir
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri algıla
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

        if faces == ():  # Yüz bulunamadıysa
            print("Yüz bulunamadı.")
            continue

        else:
            # En büyük yüzü seç
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
            x, y, w, h = largest_face
            print(f"Yüz konumu: y={y}")
            # Yüzün merkezini hesapla
            face_center_y = y + h // 2

            # Kameranın dikey çözünürlüğünün yarısı (ekranın orta noktası)
            frame_center_y = frame.shape[0] // 2

            # Yüz ekranın ortasında değilse servo motoru ayarla
            if face_center_y < frame_center_y - 50:  # Yüz yukarıdaysa
                print("Yüz yukarıda kaldı, açıyı arttırıyor.")
                move_servo(min(180, current_angle + 10))
            elif face_center_y > frame_center_y + 50:  # Yüz aşağıdaysa
                print("Yüz aşağıda kaldı, açıyı azaltıyor.")
                move_servo(max(0, current_angle - 10))

        # 'q' tuşuna basıldığında çık
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kaynakları serbest bırak
    picam2.stop()
    GPIO.cleanup()
    cv2.destroyAllWindows()

# Servo motor başlatılmadan önce ayarlanıyor
servo = GPIO.PWM(SERVO_PIN, 50)
face_recognition()
