import requests
import random
from os import environ

proxy_url = 'http://172.16.10.164:7890'

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
    proxies = get_proxy()
    def __init__(self, bot_id, chat_id='1408764137'):
        self.bot_id = bot_id
        self.chat_id = chat_id
    '''
    api 地址
    https://api.telegram.org/bot[bot_id]/sendPhoto?chat_id=[chat_id]&photo=[图片网址]?v=[随机数防止缓存]
    '''
    def send_image(self, url):
        url = 'https://api.telegram.org/bot%s/sendPhoto?chat_id=%s&photo=%s?v=%d' % (self.bot_id, self.chat_id, url, random.randint(10000000, 99999999))
        result = requests.post(url, proxies=TeleBot.proxies)
        return result

if __name__ == "__main__":
    res = TeleBot('1484376818:AAEI5hFVMt-T0ZRNgxt9ThskrDuXZd2Z0wo', '1408764137').send_image('http://j4.dfcfw.com/charts/pic6/000001.png')
    print('123')