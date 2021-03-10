import base64
import hashlib
import requests
import re
import json

class WxBot:
    '第一个参数为指令，第二个参数为机器人的key'
    BOT_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/%s?key=%s'
    FILE_UPLOAD_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key=%s&type=%s'
    FILE_UPLOAD_TYPE = 'file'
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def send_image(self, image):
        bot_url, headers, data = self.get_image_data(image)
        return requests.post(bot_url, headers=headers, json=data)
    
    def get_image_data(self, image):
        '''
        传入ByteIO对象
        '''
        encodestr = base64.b64encode(image.getvalue())
        image_data = str(encodestr, 'utf-8')
        
        # with open(image, 'rb') as file:                   #图片的MD5值
        md = hashlib.md5()
        md.update(image.getvalue())
        image_md5 = md.hexdigest()
            
        bot_url = WxBot.BOT_URL % ('send', self.bot_id)                                      #填上机器人Webhook地址 
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "image",
            "image": {
                "base64": image_data,
                "md5": image_md5
            }
        }
        return bot_url, headers, data
    
    def upload_file(self, path:str) -> dict:
        files = {'media': open(path, 'rb')}
        url = WxBot.FILE_UPLOAD_URL % (self.bot_id, WxBot.FILE_UPLOAD_TYPE)
        r = requests.post(url, files=files)
        res = json.loads(r.text)
        "{'errcode': 0, 'errmsg': 'ok', 'type': 'file', 'media_id': '3k_Jn78qRCH8pp0ftQM04rPe5jbfU7tIbkBzEE2mgcwU', 'created_at': '1615284891'}"
        return res

    def send_file(self, media_id:str) -> dict:
        bot_url = WxBot.BOT_URL % ('send', self.bot_id)
        data = {
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        }
        return requests.post(bot_url, json=data)
        
    async def async_send_image(self, image, session):
        bot_url, headers, data = self.get_image_data(image)
        async with session.post(bot_url, headers=headers, json=data) as res:
            return await res.text()