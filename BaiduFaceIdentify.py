import base64
from aip import AipFace

class BaiduFaceIdentify:
    """基于百度 API 的人脸识别类"""
    def __init__(self, APP_ID='18174994',
                 API_KEY='CPK3UVxCWFnTOL0BkyxSGWGy',
                 SECRET_KEY='23uyGD9Tu4cgfC779tjjKPdenWYGgu2O'):
        self.client = AipFace(APP_ID, API_KEY, SECRET_KEY)

    def face_check(self, image_path: str, options: dict = None) -> list:
        """
        人脸检测：检测图片中的人脸并标记出位置信息
        :param image_path: 图像路径
        :param options: face_field，max_face_num，face_type，liveness_control
        :return: 检测到输出人脸信息，否则输出 None
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        data = base64.b64encode(image_data)
        image = data.decode()
        imageType = "BASE64"
        """ 带参数调用人脸检测 """
        if not options:
            """ 如果没有可选参数 """
            options = {"face_field": "age", "max_face_num": 10}
            res = self.client.detect(image, imageType, options)
        else:
            res = self.client.detect(image, imageType)
        try:
            res_list = res['result']
        except Exception as e:
            res_list = None
            print(e)
        return res_list

    def face_search(self, image_path: str, groupIdList: str = "group1", options: dict = None) -> dict:
        """
        1：N人脸搜索：也称为1：N识别，在指定人脸集合中，找到最相似的人脸；
        1：N人脸认证：基于uid维度的1：N识别，由于uid已经锁定固定数量的人脸，所以检索范围更聚焦；
        1：N人脸识别与1：N人脸认证的差别在于：人脸搜索是在指定人脸集合中进行直接地人脸检索操作，
            而人脸认证是基于uid，先调取这个uid对应的人脸，再在这个uid对应的人脸集合中进行检索
            （因为每个uid通常对应的只有一张人脸，所以通常也就变为了1：1对比）；
            实际应用中，人脸认证需要用户或系统先输入id，这增加了验证安全度，但也增加了复杂度，具体使用哪个接口需要视您的业务场景判断。
        :param image_path: 图像路径
        :param options:
        :param groupIdList:
        :return:
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        data = base64.b64encode(image_data)
        image = data.decode()
        imageType = "BASE64"
        if not options:
            """ 如果没有可选参数 """
            options = {"quality_control": "NORMAL", "liveness_control": "LOW", "max_user_num": 3,
                       "match_threshold": 70}
            """ 带参数调用人脸搜索 """
            res = self.client.search(image, imageType, groupIdList, options)
        else:
            res = self.client.search(image, imageType, groupIdList)
        # try:
        #     res_list = res['result']
        # except Exception as e:
        #     res_list = None
        return res

    def face_login(self, image_path: str, groupId: str = 'group1', userId: str = "0", options: dict = None) -> dict:
        """
        人脸注册，用于从人脸库中新增用户，可以设定多个用户所在组，及组内用户的人脸图片
        :param image_path: 图像路径
        :param userId:
        :param groupId:
        :param options:
        :return:
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        data = base64.b64encode(image_data)
        image = data.decode()
        imageType = "BASE64"
        """ 如果没有可选参数 """
        if not options:
            options = {"user_info": "face", "quality_control": "NORMAL", "liveness_control": "LOW",
                       "action_type": "REPLACE"}
            """ 带参数调用人脸注册 """
            res = self.client.addUser(image, imageType, groupId, userId, options)
        else:
            res = self.client.addUser(image, imageType, groupId, userId)
        return res

    def face_update(self, image_path: str, groupId: str = 'group1', userId: str = '0', options: dict = None) -> dict:
        """
        人脸更新：用于对人脸库中指定用户，更新其下的人脸图像。
        :param image_path:
        :param groupId:
        :param userId:
        :param options:
        """
        with open(image_path, "rb") as f:
            image_data = f.read()
        data = base64.b64encode(image_data)
        image = data.decode()
        imageType = "BASE64"
        """ 带参数调用人脸更新 """
        if not options:
            """ 如果没有可选参数 """
            options = {"user_info": "user's info", "quality_control": "NORMAL", "liveness_control": "LOW",
                       "action_type": "REPLACE"}
            res = self.client.updateUser(image, imageType, groupId, userId, options)
        else:
            res = self.client.updateUser(image, imageType, groupId, userId)
        return res

    def get_user_list(self, groupId: str = 'group1', options: dict = None) -> dict:
        """
        获取用户列表：用于查询指定用户组中的用户列表
        :param groupId:
        :param options:
        """
        if not options:
            """ 如果没有可选参数 """
            options = {"start": 0, "length": 50}
            """ 带参数调用获取用户列表 """
            res = self.client.getGroupUsers(groupId, options)
        else:
            res = self.client.getGroupUsers(groupId)
        return res

    def delete_user(self, groupId: str = 'group1', userId: str = '0') -> dict:
        """
        删除用户：删除指定组中的用户
        :param groupId:
        :param userId:
        """
        res = self.client.deleteUser(groupId, userId)
        return res

if __name__ == "__main__":
    recongnizer = BaiduFaceIdentify()
    # res = recongnizer.face_check('others_1.jpg')
    # res = recongnizer.face_search('img/detected_face_0.jpg')
    # res = recongnizer.face_login('me.jpg', userId='ZhongWei')
    # if res_check:
    # res = recongnizer.face_update('me_1.jpg')
    # else:
    #     res_update = None
    # res = recongnizer.get_user_list()
    # res = recongnizer.delete_user(userId='ZhongWei')
    print(res)
