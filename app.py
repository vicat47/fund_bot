from dao.fund import Fund
from dao.user import User
from scheduler import MyScheduler
from wxbot import WxBot
from telebot import TeleBot
from db_util import DB

from operator import methodcaller

from flask import Flask, request, render_template, session

app = Flask(__name__)
db = DB('sqlite3', './data/my_fund.db')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/send_fund', methods=['POST'])
def send_all():
    '''
    向所有的bot发送基金曲线
    通过库中查询后提交
    因为基金图片要请求网络，所以通过基金来遍历
    '''
    res = db.select_data('select f.id, f.user_id, u.name, u.bot_id from funds f, users u where f.user_id = u.id;')
    '''
    将基金表数据整合为：{
        基金ID1 : [{用户对象}],
        基金ID2 : [{用户对象}]
    }
    '''
    funds = dict()
    users = dict()
    for r in res:
        fid = r.get('id')
        r['id'] = r.get('user_id')
        if funds.get(fid) != None:
            funds[fid].append({'users' : User(r)})
        else:
            funds[fid] = [{'users':User(r)}]
    print(funds)
    for k, v in funds.items():
        f = Fund({'id': k})
        img = f.get_fund_byte()
        img_url = f.get_fund_url()
        for u in v:
            '''
            查找users字典
            '''
            send_img = img
            ud = u['users']
            
            bot_id = u['users'].bot_id
            bot = users.get(ud.id)
            if bot == None:
                if ':' in bot_id:
                    bot = TeleBot(bot_id)
                else:
                    bot = WxBot(bot_id)
                users[ud.id] = bot
            if ':' in bot.bot_id:
                send_img = img_url
            else:
                send_img = img
            bot.send_image(send_img)
                
    return '成功'

def __init__():
    db.execute_sql('./db.sql')

if __name__ == "__main__":
    __init__()
    app.run(host='0.0.0.0', port=5000)