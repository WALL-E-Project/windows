import RPi.GPIO as GPIO
import time
import pigpio

# GPIO pin numarası (BCM numaralandırma sistemi kullanılıyor)
servo_pin = 12  # Servo motorunuzun bağlı olduğu pin numarasını buraya yazın
pulsewidth = 500

pwmpi = pigpio.pi()
pwmpi.set_mode(servo_pin, pigpio.OUTPUT)
pwmpi.set_PWM_frequency(servo_pin, 50)

# GPIO'yu ayarla
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# PWM nesnesini oluştur
pwm = GPIO.PWM(servo_pin, 50)  # 50 Hz frekans
sayac  = 0
# PWM'i başlat
pwm.start(0)

def set_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        # Sağa hareket
        set_angle(sayac)  # Orta noktadan biraz sağa
        print("Sağa hareket")
        # Sola hareket
        #set_angle(21)  # Orta noktadan biraz sola
        if sayac < 50:
            sayac = sayac + 1.5
        else:
            sayac = 0



except KeyboardInterrupt:
    print("Program kullanıcı tarafından durduruldu")
finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO temizlendi")
