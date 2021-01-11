import requests
import random
from os import environ

proxy_url = 'http://192.168.2.20:7890'

def get_proxy():
    proxies = {
        "http": environ.get('HTTP_PROXY'),
        "https" : environ.get('HTTPS_PROXY')
    }
    if proxies.get('http') == None:
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
    return proxies

class TeleBot:
    BOT_URL = 'https://api.telegram.org/bot%s'
    proxies = get_proxy()
    def __init__(self, bot_id, chat_id='1408764137'):
        self.bot_id = bot_id
        self.chat_id = chat_id
    '''
    api 地址
    https://api.telegram.org/bot[bot_id]/sendPhoto?chat_id=[chat_id]&photo=[图片网址]?v=[随机数防止缓存]
    '''
    def send_image(self, url):
        url = (TeleBot.BOT_URL + '/sendPhoto?chat_id=%s&photo=%s?v=%d') % (self.bot_id, self.chat_id, url, random.randint(10000000, 99999999))
        return requests.post(url, proxies=TeleBot.proxies)

    async def async_send_image(self, url, session):
        bot_url = (TeleBot.BOT_URL + '/sendPhoto?chat_id=%s&photo=%s?v=%d') % (self.bot_id, self.chat_id, url, random.randint(10000000, 99999999))
        async with session.post(bot_url, proxy_url=TeleBot.proxies['http']) as res:
            return await res.text()
            