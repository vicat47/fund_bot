import requests
import random

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
        bot_url = "https://oapi.dingtalk.com/robot/send?access_token=%s" % (self.bot_id)
        headers = {"Content-Type": "application/json"}
        data = {
            "msgtype": "markdown",
            "markdown": {
                "title":"基金播报",
                "text": "%s" % (text)
            }
        }
        return requests.post(bot_url, headers=headers, json=data)

    async def async_send_image(self, url, session):
        bot_url = DingBot.BOT_URL % (self.bot_id)
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