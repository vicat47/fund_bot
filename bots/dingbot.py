import requests
import random

import time
import hmac
import hashlib
import base64
import urllib.parse

import asyncio
import aiohttp

class DingBot:
    BOT_URL = 'https://oapi.dingtalk.com/robot/send?access_token=%s'
    def __init__(self, bot_id):
        self.bot_id = bot_id

    def send_image(self, url):
        bot_url, headers, data = self.get_image_data(url)
        return requests.post(bot_url, headers=headers, json=data)

    def get_image_data(self, url):
        '''
        传入URL对象
        '''
        bot_url = DingBot.BOT_URL % (self.bot_id)
        bot_url += self.get_accessed_url()
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"基金播报",
                "text": "![funds](%s?v=%d)" % (url, random.randint(10000000, 99999999))
            }
        }
        return bot_url, headers, data

    def send_markdown(self, text):
        '''
        传入马克down
        '''
        bot_url = DingBot.BOT_URL % (self.bot_id)
        bot_url += self.get_accessed_url()
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"基金播报",
                "text": "%s" % (text)
            }
        }
        return requests.post(bot_url, headers=headers, json=data)

    def get_accessed_url(self):
        timestamp = str(round(time.time() * 1000))
        secret = 'SEC0778946039e794a42fb6eff43836316cd1c8405bc6147354124b31e1ea26329c'
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return '&timestamp=' + timestamp + '&sign=' + sign

    async def async_send_image(self, url, session):
        bot_url = DingBot.BOT_URL % (self.bot_id)
        bot_url += self.get_accessed_url()
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"基金播报",
                "text": "![funds](%s?v=%d)" % (url, random.randint(10000000, 99999999))
            }
        }
        async with session.post(bot_url, json=data, headers=headers) as res:
            return await res.text()