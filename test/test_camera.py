import time
from picamera import PiCamera

# Kamera nesnesini oluştur
camera = PiCamera()

# Kamera ayarları (isteğe bağlı)
camera.resolution = (640, 480)  # Çözünürlük ayarı

# Kamerayı başlat
camera.start_preview()
time.sleep(2)  # Önizlemenin başlaması için biraz bekle

# Fotoğraf çek ve kaydet
camera.capture('test_image.jpg')  # Fotoğrafın kaydedileceği yol
print("Fotoğraf çekildi ve kaydedildi.")

# Önizlemeyi kapat
camera.stop_preview()

# Kamerayı serbest bırak
camera.close()
