import io
import logging
import socketserver
from threading import Condition, Thread
from http import server
from picamera2 import Picamera2
from PIL import Image
import cv2
import time
import RPi.GPIO as GPIO


# Çözünürlüğü burada tanımlıyoruz
RESOLUTION = (640, 480)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
SERVO_PIN = 12
GPIO.setup(SERVO_PIN, GPIO.OUT)
servo = GPIO.PWM(SERVO_PIN, 50)
servo.start(0)  # Başlangıç pozisyonu 0 derece

servoPosition = 90
last_servo_position = None  # Son servo pozisyonunu sakla

PAGE = f"""\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="{RESOLUTION[0]}" height="{RESOLUTION[1]}"></center>
</body>
</html>
"""

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

def set_servo_angle(angle):
    global last_servo_position
    duty = 2.5 + (angle / 18)
    if last_servo_position != angle:  # Sadece açıyı değiştir
        servo.ChangeDutyCycle(duty)
        print(f"Servo açısı: {angle} derece")
        last_servo_position = angle  # Son açıyı güncelle

def capture_image_with_face_detection(picam2):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    image = picam2.capture_array()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    with output.condition:
        output.buffer = io.BytesIO()
        Image.fromarray(gray).save(output.buffer, format='JPEG')
        output.frame = output.buffer.getvalue()
        output.condition.notify_all()

    if len(faces) > 0:
        largest_face = max(faces, key=lambda rect: rect[2] * rect[3])
        x, y, w, h = largest_face
        cv2.rectangle(gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
        center_y_coord = y + h // 2
        return center_y_coord
    else:
        print("Yüz tespit edilemedi.")
        return None

picam2 = Picamera2()
picam2_config = picam2.create_still_configuration(main={"size": RESOLUTION})
picam2.configure(picam2_config)
picam2.start()

output = StreamingOutput()

def stream_loop():
    global servoPosition
    while True:
        face_y = capture_image_with_face_detection(picam2)
        if face_y is not None:
            print(f"Yüzün y koordinatı: {face_y}")
            if face_y < RESOLUTION[1] // 2:
                print("Yüz ekranın üst yarısında.")
                servoPosition = min(180, servoPosition + 10)
            elif face_y > RESOLUTION[1] // 2:
                print("Yüz ekranın alt yarısında.")
                servoPosition = max(0, servoPosition - 10)
            set_servo_angle(servoPosition)

        time.sleep(0.1)

try:
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    logging.info("Server started at http://localhost:8000")
    
    Thread(target=stream_loop, daemon=True).start()
    
    server.serve_forever()
finally:
    picam2.stop()
