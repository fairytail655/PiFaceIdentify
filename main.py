import cv2
import os
import time
from threads import ThreadSearchFace, ThreadSendEmai

cascade_path = os.path.realpath('haarcascade_frontalface_default.xml')
faceCascade = cv2.CascadeClassifier(cascade_path)

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # set Width
cap.set(4, 480)  # set Height

def create_threads_list():
    threads_baidu_list = []
    for i in range(3):
        threads_baidu_list.append(ThreadSearchFace('img/detected_face_' + str(i) + '.jpg'))
    return threads_baidu_list

thread_email = ThreadSendEmai()
threads_baidu_list = create_threads_list()
thread_count = 0
thread_baidu_end_flag = True
thread_email_end_flag = True

start_time = 0
time_end_flag = True

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
        if thread_baidu_end_flag and thread_email_end_flag and time_end_flag:
            count = 0
            for (x, y, w, h) in faces:
                cv2.rectangle(img_show, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_image = img[max(0, y - 20):min(y + h + 20, 480), max(0, x - 20):min(x + w + 20, 640)]
                img_face_path = 'img/detected_face_' + str(count) + '.jpg'
                # img_full_path = 'img/detected_full_' + str(count) + '.jpg'
                cv2.imwrite(img_face_path, face_image)
                # cv2.imwrite(img_full_path, img_show)
                count += 1
            thread_count = 0
            for i in range(min(count, 3)):
                print('开启baidu线程:%d' % i)
                thread_baidu_end_flag = False
                threads_baidu_list[i].start()
                thread_count += 1
        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(img_show, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 百度线程启动过
    if not thread_baidu_end_flag:
        # 重置百度线停止程标志位为　True
        thread_baidu_end_flag = True
        # 检查每一个百度线程，如有未执行完的则置标志位为 Fasle
        for thread in threads_baidu_list:
            if thread.is_alive():
                thread_baidu_end_flag = False
        # 百度线程全部运行完毕
        if thread_baidu_end_flag:
            print('baidu线程运行完毕')
            alert_flag = True
            stranger_image_list = []
            face_count = 0
            # 对每个百度线程检查是否检测到熟人（默认认为全部是陌生人）
            for i in range(thread_count):
                thread = threads_baidu_list[i]
                # 检测到熟人
                if thread.find_flag:
                    alert_flag = False
                elif thread.face_flag:
                    stranger_image_list.append(thread.image_path)
                # 没有检测到人脸
                if not thread.face_flag:
                    face_count += 1
            # 没有检测到人脸
            if face_count == thread_count:
                alert_flag = False
            # 没有检测到熟人且检测到人脸
            if alert_flag:
                print('检测到陌生人，已发送邮件')
                # 通过邮箱发送每个陌生人的照片
                thread_email.images_path_list = stranger_image_list
                thread_email.start()
                thread_email_end_flag = False
            else:
                print('没有检测到陌生人')
            # 重新创建所有的百度线程
            threads_baidu_list = create_threads_list()

    # 邮箱线程运行过
    if not thread_email_end_flag:
        thread_email_end_flag = True
        # 检查邮箱线程，如有未执行完的则置标志位为 Fasle
        if thread_email.is_alive():
            thread_email_end_flag = False
        # 邮箱线程运行完毕
        if thread_email_end_flag:
            print('邮箱线程运行完毕')
            # 重新创建所有需要的线程
            thread_email = ThreadSendEmai()
            # 开始计时
            print('开始计时')
            start_time = time.time()
            time_end_flag = False

    # 开始计时
    if not time_end_flag:
        end_time = time.time()
        # 时间间隔大于 10 s
        if end_time - start_time > 20:
            time_end_flag = True
            print('时间到了')

    # cv2.imshow('img', img_show)

    # k = cv2.waitKey(10) & 0xff
    # if k == 27:  # press 'ESC' to quit
    #     break

# cap.release()
# cv2.destroyAllWindows()
