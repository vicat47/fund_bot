import base64
import hashlib
import requests

class WxBot:
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def send_image(self, image):
        '''
        传入ByteIO对象
        '''
        encodestr = base64.b64encode(image.getvalue())
        image_data = str(encodestr, 'utf-8')
        
        # with open(image, 'rb') as file:                   #图片的MD5值
        md = hashlib.md5()
        md.update(image.getvalue())
        image_md5 = md.hexdigest()
            
        url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=%s" % (self.bot_id)                                      #填上机器人Webhook地址 
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_data,
                "md5": image_md5
            }
        }
        return requests.post(url, headers=headers, json=data)