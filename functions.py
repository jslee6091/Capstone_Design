import cv2
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import tensorflow as tf


font = cv2.FONT_HERSHEY_SIMPLEX
face_detector = cv2.CascadeClassifier('Utils/haarcascade_frontface.xml')

model = tf.keras.models.load_model("models/face_model0512.h5")
id = ["Deukhwa", "Joohyeong", "Jeasung", "Unknown"]


def face_recognize():
    img_pred_path = 'Faces/'
    pred_datagen = ImageDataGenerator(rescale=1. / 255)
    pred_generator = pred_datagen.flow_from_directory(img_pred_path, target_size=(224, 224),
                                                      color_mode='grayscale', batch_size=1, class_mode='categorical')
    output = model.predict(pred_generator, steps=1)
    index = np.argmax(output)
    accu = str(round(np.max(output) * 100, 2))
    name = id[index]
    print(name, accu + "%")
    return name, accu


# capture user's face and save
def cam_shot():
    cam = cv2.VideoCapture(0)
    cnt = 0

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite("Faces/Pred/" + "face" + ".jpg", gray[y:y + h, x:x + w])
            cnt += 1

        if cnt == 1:
            break

    cam.release()
    cv2.destroyAllWindows()
