from dao.fund import Fund
from dao.user import User
# from scheduler import MyScheduler
from bots.wxbot import WxBot
from bots.telebot import TeleBot
from db_util import DB
import services

from flask import Flask, request, render_template, session

import json

app = Flask(__name__)
db = DB('sqlite3', './data/my_fund.db')

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/publish_fund_image/<int:user_id>', methods=['POST'])
def publish_user_funds(user_id):
    user = None
    try:
        user = next(db.select_data('select * from users where id = %d' % (user_id)))
    except StopIteration:
        return '没有id为%d的用户' % (user_id)
    else:
        if user == None:
            return '没有该用户' % (user_id)
    funds = db.select_data('select * from funds where user_id = %d;' % (user_id))
    bot = services.get_bot(user.get('bot_id'), user.get('chat_id'))
    for fund in funds:
        f = Fund(fund.get('id'))
        services.send_fund_image(bot, f)
    return '成功'

@app.route('/publish_fund_image/<name>', methods=['POST'])
def publish_fund_image_by_name(name):
    user = None
    try:
        user = next(db.select_data('select * from users where name = "%s"' % (name)))
    except StopIteration:
        return '没有用户名为%s的用户' % (name)
    else:
        if user == None:
            return '没有用户名为%s的用户' % (name)
    funds = db.select_data('select * from funds where user_id = %d;' % (user.get('id')))
    bot = services.get_bot(user.get('bot_id'), user.get('chat_id'))
    for fund in funds:
        f = Fund(fund.get('id'))
        services.send_fund_image(bot, f)
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
    构造bot字典：{
        bot_id-chat_id : Bot对象
    }
    '''
    funds = generate_fund_userlist(res)
    bots = dict()
    print(funds)
    for fund_id, user_list in funds.items():
        f = Fund(fund_id)
        for user in user_list:
            '''
            查找bots字典
            '''
            bid, cid = user.get('bot_id'), user.get('chat_id')
            bot_key = '%s-%s' % (bid, cid)
            bot = bots.get(bot_key)
            if bot == None:
                bot = bots[bot_key] = services.get_bot(bid, cid)
            services.send_fund_image(bot, f)
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