import cv2
import os
from BaiduFaceIdentify import BaiduFaceIdentify
from threads import ThreadSearchFace

cascade_path = os.path.realpath('haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cascade_path)

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height

identify = BaiduFaceIdentify()

thread_count = 0
def create_threads_list():
    threads_list = []
    for i in range(3):
        threads_list.append(ThreadSearchFace('img/detected_face_' + str(i) + '.jpg'))
    return threads_list
threads_list = create_threads_list()

while True:
    ret, img = cap.read()
    img_show = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # faces 为坐标列表,如　[[266 230 227 227]]
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(20, 20)
    )
    # 如果检测到人脸
    if len(faces):
        if thread_count == 0:
            count = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(img_show, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_image = img[max(0, y - 20):min(y + h + 20, 480), max(0, x - 20):min(x + w + 20, 640)]
                img_path = 'img/detected_face_' + str(count) + '.jpg'
                cv2.imwrite(img_path, face_image)
                count += 1
            for i in range(min(count, 3)):
                threads_list[i].start()
                thread_count += 1
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(img_show, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if thread_count != 0:
        thread_end_flag = False
        for thread in threads_list:
            if thread.is_alive():
                thread_end_flag = True
        if not thread_end_flag:
            thread_count = 0
            alert_flag = True
            for thread in threads_list:
                if thread.find_flag:
                    alert_flag = False
            if alert_flag:
                print('检测到陌生人')
            else:
                print('没有检测到陌生人')
            threads_list = create_threads_list()

    cv2.imshow('img', img_show)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
