import requests
import random

# proxy_ip = '127.0.0.1'
proxy_ip = '172.16.10.164'

proxies = {
  "http": "http://%s:7890" % (proxy_ip),
  "https": "http://%s:7890" % (proxy_ip),
}

class TeleBot:
    def __init__(self, bot_id):
        self.bot_id = bot_id
    '''
    api 地址
    https://api.telegram.org/bot1484376818:AAEI5hFVMt-T0ZRNgxt9ThskrDuXZd2Z0wo/sendPhoto?chat_id=843372582&photo=http://j4.dfcfw.com/charts/pic6/161725.png
    '''
    def send_image(self, url):
        url = 'https://api.telegram.org/bot%s/sendPhoto?chat_id=1408764137&photo=%s?v=%d' % (self.bot_id, url, random.randint(10000000, 99999999))
        result = requests.post(url, proxies=proxies)
        return result

if __name__ == '__main__':
    bot = TeleBot('1484376818:AAEI5hFVMt-T0ZRNgxt9ThskrDuXZd2Z0wo')
    bot.send_image('http://j4.dfcfw.com/charts/pic6/161725.png')
