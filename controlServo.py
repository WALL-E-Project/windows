# # gpt ile sesli komutlar ile servo kontrolü
# # 20.11.2024    

# import speech_recognition as sr
# import RPi.GPIO as GPIO
# import time
# import pigpio

# # Initialize pigpio
# pwm = pigpio.pi()
# if not pwm.connected:
#     print("Pigpio daemon is not running!")
#     exit()

# # Configure servo
# servo_pin = 12  # Same pin as in other files
# pulsewidth = 750  # Initial position
# pwm.set_mode(servo_pin, pigpio.OUTPUT)
# pwm.set_PWM_frequency(servo_pin, 50)

def control_servo(command):
    """
    Servo motorunu yukarı veya aşağı hareket ettiren fonksiyon.
    
    Args:
        command (str): Hareket komutu ('up'/'yukarı' veya 'down'/'aşağı')
    
    Returns:
        bool: İşlemin başarılı olup olmadığını belirten değer
    """
    global pulsewidth
    
    try:
        if not isinstance(command, str):
            print("Hata: Komut string tipinde olmalıdır.")
            return False
            
        command = command.lower()
        step_size = 75  # Her adımda hareket miktarı
        
        # Hareket yönüne göre pulse genişliğini ayarla
        if "yukarı" in command or "up" in command:
            pulsewidth = min(pulsewidth + step_size, 2500)  # Üst limit kontrolü
            print("Yukarı Aldı Kafayı")
        elif "aşağı" in command or "down" in command:
            pulsewidth = max(pulsewidth - step_size, 500)   # Alt limit kontrolü
            print("Aşşağı Aldı Kafayı")

        else:
            print("Hata: Geçersiz hareket komutu. 'up' veya 'down' kullanın.")
            return False
            
        # Servo pozisyonunu güncelle
        # pwm.set_servo_pulsewidth(servo_pin, pulsewidth)
        print(f"Servo pozisyonu güncellendi. Yeni pulse genişliği: {pulsewidth}")
        return True
        
    except Exception as e:
        print(f"Servo kontrolünde hata oluştu: {str(e)}")
        return False
