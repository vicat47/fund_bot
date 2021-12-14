from dao.fund import Fund
from dao.user import User
# from scheduler import MyScheduler
from bots.wxworkbot import WxWorkBot
from bots.telebot import TeleBot
from utils import DB
import services

import asyncio

from flask import Flask, request, render_template, session

import json
import logging

app = Flask(__name__)
logger = logging.getLogger('flask.app')
loop = asyncio.get_event_loop()
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
        return {'status' : 'error', 'message' : '没有id为%d的用户' % (user_id)}
    else:
        if user == None:
            return {'status' : 'error', 'message' : '没有该用户' % (user_id)}
    funds = db.select_data('select * from funds where user_id = %d;' % (user_id))
    bot = services.get_bot(user.get('bot_id'), user.get('chat_id'))
    for fund in funds:
        f = Fund(fund.get('id'))
        res = services.send_fund_image(bot, f)
    return res.text

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
        res = services.send_fund_image(bot, f)
    return res.text

@app.route('/publish_fund_image/async/<name>', methods=['POST'])
def async_publish_fund_image_by_name(name):
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
    tasks = [services.async_send_image(bot, Fund(f.get('id'))) for f in funds]
    group = asyncio.gather(*tasks, loop=loop)
    res = loop.run_until_complete(group)
    return str(res)

@app.route('/publish_fund_image/async', methods=['POST'])
def publish_fund_image_async():
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
    tasks = []
    print(funds)
    for fund_id, user_list in funds.items():
        f = Fund(fund_id)
        for user in user_list:
            '''
            查找bots字典
            '''
            bid, cid = user.bot_id, user.chat_id
            bot_key = '%s-%s' % (bid, cid)
            bot = bots.get(bot_key)
            if bot == None:
                bot = bots[bot_key] = services.get_bot(bid, cid)
            tasks.append(services.async_send_image(bot, f))
    group = asyncio.gather(*tasks, loop=loop)
    res = loop.run_until_complete(group)
    return str(res)

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
            bid, cid = user.bot_id, user.chat_id
            bot_key = '%s-%s' % (bid, cid)
            bot = bots.get(bot_key)
            if bot == None:
                bot = bots[bot_key] = services.get_bot(bid, cid)
            services.send_fund_image(bot, f)
    return '成功'

@app.route('/users', methods=['GET'])
def get_users():
    users = list(db.select_data('select * from users'))
    return str([(u.get('id'), u.get('name')) for u in users])


@app.route('/users/<int:user_id>/funds', methods=['GET'])
def get_user_funds(user_id):
    res = list(db.select_data('select * from funds where user_id=%d;' % (user_id)))
    return str([f.get('id') for f in res])


@app.route('/users/<int:user_id>/funds', methods=['POST'])
def add_user_funds(user_id):
    'TODO'
    data = json.loads(request.get_data(as_text=True))
    return json.dumps([db.insert_data('funds', d) for d in data])

@app.route('/users/<int:user_id>/funds/<fund_id>', methods=['POST'])
def add_user_fund(user_id, fund_id):
    return db.insert_data('funds', {'id': fund_id, 'user_id': user_id})

@app.route('/users/<int:user_id>/funds/<fund_id>', methods=['DELETE'])
def del_user_fund(user_id, fund_id):
    return db.delete_data('funds', {'id': fund_id, 'user_id': user_id})

@app.route('/users/<int:user_id>/funds', methods=['DELETE'])
def del_user_funds(user_id):
    data = json.loads(request.get_data(as_text=True))
    return [db.delete_data('funds', d) for d in data]

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