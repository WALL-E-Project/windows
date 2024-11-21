#!/usr/bin/python3
import pigpio
import time

servo = 12
pulsewidth = 500

pwm = pigpio.pi()
if not pwm.connected:
    print("Pigpio daemon is not running!")
    exit()

pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)

try:
    while True:
        print(f"Pulsewidth: {pulsewidth}")
        pwm.set_servo_pulsewidth(servo, pulsewidth)
        pulsewidth += 15
        if pulsewidth > 1250:  # Maksimum değer
            pulsewidth = 500  # Minimuma döndür
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    pwm.set_servo_pulsewidth(servo, 0)  # Servo'yu kapat
    pwm.stop()
