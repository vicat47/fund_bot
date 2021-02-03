import bots
import asyncio
import aiohttp

session = aiohttp.ClientSession()

def get_bot(bot_id, chat_id=None):
    if len(bot_id) == 64:
        return bots.DingBot(bot_id, chat_id)
    elif chat_id == None:
        return bots.WxBot(bot_id)
    else:
        return bots.TeleBot(bot_id, chat_id)

def send_fund_image(bot, fund):
    return send_image(bot, get_fund_img(bot, fund))

def send_image(bot, img):
    return bot.send_image(img)

def get_fund_img(bot, fund):
    if isinstance(bot, bots.WxBot):
        return fund.get_fund_byte()
    else:
        return fund.get_fund_url()

async def aget_fund_img(bot, fund):
    if isinstance(bot, bots.WxBot):
        return await fund.aget_fund_byte(session)
    else:
        return fund.get_fund_url()

async def async_send_image(bot, fund):
    return await bot.async_send_image(await aget_fund_img(bot, fund), session)
