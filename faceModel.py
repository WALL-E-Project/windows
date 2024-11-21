import cv2
from deepface import DeepFace

"""
todo:
1. face_recognation fonksiyonunu düzenle
2. multi treading ile yüz tanıma işlemini hızlandır
3. tekli yüz tanıma işlemi yap
4. hızlandırma yöntemlerini araştır
"""

def recognize_faces(face_img):
    result = DeepFace.find(img_path=face_img, db_path="faces/", enforce_detection=False)
    return result

def analyze_faces(face_img):
    analysis = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
    return analysis


def face_recognation():
    face_cascade = cv2.CascadeClassifier('faces/haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Yüzleri algılama
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

         # En büyük yüzü seç
        if faces == ():
            print("Yüz bulunamadı")
        
        else:
            largest_face = max(faces, key=lambda rect: rect[2] * rect[3])


            x, y, w, h = largest_face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            face_img = frame[y:y+h, x:x+w]

            cv2.imshow('Face detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

face_recognation()
