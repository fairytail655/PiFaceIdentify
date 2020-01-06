import threading
from BaiduFaceIdentify import BaiduFaceIdentify


class ThreadSearchFace(threading.Thread):
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        self.identify = BaiduFaceIdentify()
        self.find_flag = False

    def run(self) -> None:
        check_res = self.identify.face_check(self.image_path)
        if check_res:
            search_res = self.identify.face_search(self.image_path)
            print(search_res)
            if search_res['error_code'] == 0:
                self.find_flag = True
            else:
                self.find_flag = False
        else:
            self.find_flag = False
