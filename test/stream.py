import io
import logging
import socketserver
from threading import Condition, Thread
from http import server
from picamera2 import Picamera2
from PIL import Image
import cv2
import time
from cvzone.FaceDetectionModule import FaceDetector
import RPi.GPIO as GPIO
import pigpio

# bu kod çalışıyor 20.11.2024
pulsewidth = 750
pwmpi = pigpio.pi()


servo_pin = 12  # Servo motorunuzun bağlı olduğu pin numarasını buraya yazın

# GPIO'yu ayarla
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(servo_pin, GPIO.OUT)

pwmpi.set_mode(servo_pin, pigpio.OUTPUT)
pwmpi.set_PWM_frequency(servo_pin, 50)

#pwmpi.set_servo_pulsewidth(servo_pin, pulsewidth)

# PWM nesnesini oluştur
#pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frekans
derece = 15
# PWM'i başlat
#pwm.start(0)

detector = FaceDetector()

# Çözünürlüğü burada tanımlıyoruz
RESOLUTION = (1280, 720)  # (genişlik, yükseklik)  640x480, 1280x720, 1920x1080, 2592x1944

PAGE = f"""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="{RESOLUTION[0]}" height="{RESOLUTION[1]}"></center>  <!-- Çözünürlük buradan alınacak -->
</body>
</html>
"""
def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)



class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning('Removed streaming client %s: %s', self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Yüz tanıma ve en büyük yüzü çerçeveleme
def capture_image_with_face_detection(picam2):
    # Haarcascade modelini yüklüyoruz
    img = picam2.capture_array()
    img, bboxs = detector.findFaces(img)

    if bboxs:
        x1, y1, w1, h1 = bboxs[0]['bbox']
        cv2.rectangle(img, (x1, y1), (x1+w1, y1+h1), (255, 0, 255), 2)
        center1 = bboxs[0]['center']
        y_medium = center1[1]
        cv2.circle(img, center1, 5, (0, 255, 0), cv2.FILLED)
        #print(center1)
        print(y_medium // 62)
        return y_medium // 62


    """face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Görüntüyü RGB formatına çeviriyoruz
    gray = image #cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # x ve y cizgileri cizdir
    #cv2.line(gray, (gray.shape[1] // 2, 0), (gray.shape[1] // 2, gray.shape[0]), (255, 0, 0), 2) 
    #cv2.line(gray, (0, gray.shape[0] // 2), (gray.shape[1], gray.shape[0] // 2), (255, 0, 0), 2)  
    

    # Eğer yüzler tespit edildiyse
    if len(faces) > 0:
        # En büyük alanı kaplayan yüzü seçiyoruz
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Gri görüntüde mavi yerine beyaz kare çizer
        
        # Yüzün merkezini hesaplayın
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Merkeze küçük bir daire çiz
        cv2.circle(gray, (center_x, center_y), radius=5, color=(255, 0, 0), thickness=-1)
    """



    # Gri tonlamalı resmi JPEG formatına çeviriyoruz
    with output.condition:
        output.buffer = io.BytesIO()
        Image.fromarray(img).save(output.buffer, format='JPEG')
        output.frame = output.buffer.getvalue()
        output.condition.notify_all()

# Picamera2 ile Kamera başlatma
picam2 = Picamera2()

# Çözünürlüğü arttırmak için tanımlanan RESOLUTION değişkeni kullanılıyor
picam2_config = picam2.create_still_configuration(main={"size": RESOLUTION})
picam2.configure(picam2_config)
picam2.start()

# Akışın çıkışı için StreamingOutput sınıfını oluştur
output = StreamingOutput()

# Her 0.1 saniyede bir yeni görüntü yakalayıp yüzleri tanıyacağız
def stream_loop():
    global derece
    global pulsewidth
    global yuz_konumu_y
    global pwmpi
    global servo_pin
    while True:
        
        yuz_konumu_y = capture_image_with_face_detection(picam2)
        if yuz_konumu_y != None:
            if 0 < yuz_konumu_y < 6:
                #yöntem 1   
                #derece +=2.5    
                #set_angle(derece)    
                
                #yöntem 2
                pulsewidth +=15
                print("pulsewidth:",pulsewidth)
                if pulsewidth > 2500:
                    pulsewidth = 2500
                elif pulsewidth < 500:
                    pulsewidth = 500

                pwmpi.set_servo_pulsewidth(servo_pin, pulsewidth)
                
                

            elif 6 < yuz_konumu_y < 12:

                #yöntem 1
                #derece -=2.5
                #set_angle(derece)

                #yöntem 2
                pulsewidth -=15
                print("pulsewidth:",pulsewidth)
                if pulsewidth > 2500:
                    pulsewidth = 2500
                elif pulsewidth < 500:
                    pulsewidth = 500

                pwmpi.set_servo_pulsewidth(servo_pin, pulsewidth)
                
                
                
        print("yuz_konumu_y:",yuz_konumu_y)
        #print("derece:",derece)
        time.sleep(0.05)

# Streaming server'ı başlat
try:
    address = ('', 8000)
    logging.basicConfig(level=logging.INFO)

    # capture_image_with_face_detection içinde
    logging.info("Capturing image and performing face detection")

    # stream_loop içinde
    logging.info("Streaming loop is running")
    server = StreamingServer(address, StreamingHandler)
    logging.info("Server started at http://localhost:8000")
    
    # Görüntü yakalamayı ve yüz tanımayı ayrı bir thread'de çalıştır
    Thread(target=stream_loop, daemon=True).start()
    
    server.serve_forever()
finally:
    picam2.stop()
