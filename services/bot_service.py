import bots

def get_bot(bot_id, chat_id=None):
    if chat_id == None:
        return bots.WxBot(bot_id)
    else:
        return bots.TeleBot(bot_id, chat_id)

def send_fund_image(bot, fund):
    send_image(bot, get_fund_img(bot, fund))

def send_image(bot, img):
    bot.send_image(img)

def get_fund_img(bot, fund):
    if isinstance(bot, bots.TeleBot):
        return fund.get_fund_url()
    else:
        return fund.get_fund_byte()