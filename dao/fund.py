import requests, asyncio, aiohttp
# from PIL import Image
from io import BytesIO
import math, time

class Fund:
    '''
    需要一个基金ID
    '''
    def __init__(self, fund_id):
        self.id = fund_id
        self.cache = None

    def get_fund_url(self):
        return 'http://j4.dfcfw.com/charts/pic6/%s.png' % (self.id)

    def get_fund_data(self):
        return requests.get('http://j4.dfcfw.com/charts/pic6/%s.png' % (self.id))
    
    def get_fund_byte(self):
        if self.cache == None:
            self.cache = self.get_fund_data().content
        return BytesIO(self.cache)

    async def get_fund_curr(self, session):
        async with session.get('http://fundgz.1234567.com.cn/js/%s.js?rt=%d' % (self.id, math.floor(time.time() * 1000))) as res:
            return await res.text()

    async def aget_fund_byte(self, session):
        if self.cache == None:
            async with session.get('http://j4.dfcfw.com/charts/pic6/%s.png' % (self.id)) as res:
                self.cache = await res.read()
                return BytesIO(self.cache)
                
    # def get_fund_img(self, fund_id):
    #     return Image.open(BytesIO(self.get_fund_data(fund_id).content))
