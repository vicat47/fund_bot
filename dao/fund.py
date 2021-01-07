import requests
# from PIL import Image
from io import BytesIO

class Fund:
    '''
    需要一个基金ID
    '''
    def __init__(self, data):
        self.id = data.get('id')

    def get_fund_url(self):
        return 'http://j4.dfcfw.com/charts/pic6/%s.png' % (self.id)

    def get_fund_data(self):
        return requests.get('http://j4.dfcfw.com/charts/pic6/%s.png' % (self.id))
    
    def get_fund_byte(self):
        return BytesIO(self.get_fund_data().content)

    # def get_fund_img(self, fund_id):
    #     return Image.open(BytesIO(self.get_fund_data(fund_id).content))
