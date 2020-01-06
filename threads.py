import threading
from BaiduFaceIdentify import BaiduFaceIdentify
from PostMail import Email


class ThreadSearchFace(threading.Thread):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.identify = BaiduFaceIdentify()
        self.find_flag = False
        self.face_flag = True

    def run(self) -> None:
        check_res = self.identify.face_check(self.image_path)
        if check_res:
            self.face_flag = True
            search_res = self.identify.face_search(self.image_path)
            print(search_res)
            if search_res['error_code'] == 0:
                self.find_flag = True
            else:
                self.find_flag = False
        else:
            self.face_flag = False
            self.find_flag = False

class ThreadSendEmai(threading.Thread):
    def __init__(self):
        super().__init__()
        self.images_path_list = []

    def run(self) -> None:
        mail_msg = """
        <p>警告，检测到陌生人，请注意！</p>
        <p>陌生人照片</p>
        """
        self.email = Email(
            smtp_server='smtp.163.com',
            from_addr='fox_benjiaming@163.com',
            password='Kaisa9130',
            to_addr='2623538943@qq.com',
            type='html',
            title='邮件发送实验',
            content=mail_msg,
            images_path_list=self.images_path_list
        )
        print(self.email.send_msg())
