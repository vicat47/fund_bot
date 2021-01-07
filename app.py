from dao.fund import Fund
from dao.user import User
from scheduler import MyScheduler
from bots.wxbot import WxBot
from bots.telebot import TeleBot
from db_util import DB

from flask import Flask, request, render_template, session
import json

app = Flask(__name__)
db = DB('sqlite3', './data/my_fund.db')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/publish_fund_image/<int:user_id>', methods=['POST'])
def push_user_funds(user_id):
    user = next(db.select_data('select * from users where id = %d' % (user_id)))
    funds = db.select_data('select * from funds where user_id = %d;' % (user_id))
    bot_id = user.get('bot_id')
    bot = None
    'WX: 0, TELE: 1'
    bot_type = 0
    if ':' in bot_id:
        bot = TeleBot(bot_id, user.get('chat_id'))
        bot_type = 1
    else:
        bot = WxBot(bot_id)
        bot_type = 0
    for fund in funds:
        f = Fund({'id' : fund.get('id')})
        if bot_type == 0:
            bot.send_image(f.get_fund_byte())
        else:
            bot.send_image(f.get_fund_url())
    return '成功'

@app.route('/publish_fund_image/name/<name>', methods=['POST'])
def publish_fund_image_by_name(name):
    user = next(db.select_data('select * from users where name = "%s"' % (name)))
    funds = db.select_data('select * from funds where user_id = %d;' % (user.get('id')))
    bot_id = user.get('bot_id')
    bot = None
    'WX: 0, TELE: 1'
    bot_type = 0
    if ':' in bot_id:
        bot = TeleBot(bot_id, user.get('chat_id'))
        bot_type = 1
    else:
        bot = WxBot(bot_id)
        bot_type = 0
    for fund in funds:
        f = Fund({'id' : fund.get('id')})
        if bot_type == 0:
            bot.send_image(f.get_fund_byte())
        else:
            bot.send_image(f.get_fund_url())
    return '成功'

@app.route('/publish_fund_image', methods=['POST'])
def publish_fund_image():
    '''
    向所有的bot发送基金曲线
    通过库中查询后提交
    因为基金图片要请求网络，所以通过基金来遍历
    '''
    res = db.select_data('select f.id, f.user_id, u.name, u.bot_id, u.chat_id from funds f, users u where f.user_id = u.id;')
    '''
    将基金表数据整合为：{
        基金ID1 : [{用户对象}],
        基金ID2 : [{用户对象}]
    }
    并构造bot字典：{
        用户id : Bot对象
    }
    '''
    funds = generate_fund_userlist(res)
    bots = dict()
    print(funds)
    for k, v in funds.items():
        f = Fund({'id': k})
        img = f.get_fund_byte()
        img_url = f.get_fund_url()
        for u in v:
            '''
            查找bots字典
            '''
            send_img = img
            bot_id = u.bot_id
            bot = bots.get(u.id)
            if bot == None:
                if ':' in bot_id:
                    bot = TeleBot(bot_id, u.chat_id)
                else:
                    bot = WxBot(bot_id)
                bots[u.id] = bot
            if ':' in bot.bot_id:
                send_img = img_url
            else:
                send_img = img
            bot.send_image(send_img)
    return '成功'

def generate_fund_userlist(data):
    '''
    将基金表数据整合为：{
        基金ID1 : [{用户对象}],
        基金ID2 : [{用户对象}]
    }
    '''
    fund_user = {}
    for r in data:
        fid = r.get('id')
        r['id'] = r.get('user_id')
        if fund_user.get(fid) != None:
            fund_user[fid].append(User(r))
        else:
            fund_user[fid] = [User(r)]
    return fund_user

def __init__():
    db.execute_sql('./db.sql')

if __name__ == "__main__":
    __init__()
    app.run(host='0.0.0.0', port=5000)