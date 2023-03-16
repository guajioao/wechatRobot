

class user():
    user_id = ''
    user_info = {}

    def __init__(self,wx_id='',info={}):
        if wx_id:
            self.user_id = wx_id
            #判断info非空
            if info:
                self.user_info = info
            else:
                user_info = self._getInfo(wx_id)
                self.user_info = user_info
        else:
            print("wx_id为空!")

    
    def _getInfo(self,wx_id=''):
        print("get %s Info",wx_id)
        #从数据库根据wxid查找信息
        #假装找到了文件助手(默认)
        info={
            'wx_id': 'filehelper',
            'block': 8,
            'room': 401
        }
        return info
