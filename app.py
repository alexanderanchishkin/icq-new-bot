import os
import time
import numpy as np

from random import randrange

from utilities import idle
from utilities.db_explorer import *
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler

import json

# 001.3146970085.4148216257:752501352 main token
# (set BOT_TOKEN=001.3146970085.4148216257:752501352) && python app.py
# command for run:
# (set BOT_TOKEN=<your_bot_token>) && python app.py

TOKEN = os.getenv('BOT_TOKEN')
if TOKEN is None:
    print('Set ENV variable BOT_TOKEN')
    print('Use run command on Windows: (set BOT_TOKEN=<your_bot_token>) && python app.py')
    exit(0)

bot = Bot(token=TOKEN)
explorer = DBExplorer()

commands = ["/random", "/start", "/advice", "/get_top_advices", "get_next_advice"]

actions = [
    [{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
    [{"text": "Проветрить комнату", "callbackData": "room"}],
    [{"text": "Выпить чай с лимоном", "callbackData": "lemon"}],
    [{"text": "Отсидеться на дома", "callbackData": "home"}],
    [{"text": "Провести влажную уборку", "callbackData": "cleaning"}],
    [{"text": "Прочистить трубу", "callbackData": "truba"}],
    [{"text": "Сделать чесночный киндер", "callbackData": "onion"}],
]

def send_alerts(chats, text):
    for chat in chats:
        bot.send_text(chat_id=chat, text=text)
def get_exp(total):
    acc = 0
    lvl = 1
    aim = 80
    while total >= aim:
        total -= aim
        aim += lvl*20
        lvl += 1
    count = int((total/aim)*10)
    loader = "🌚"*count+"🌝"*(10-count)
    return {"last": total, "aim": aim, "lvl": lvl, "loader":loader}
def updateMessages(bot, chat_id, msg_id, text, markup=None):
    response = bot.edit_text(chat_id=chat_id, msg_id=msg_id, 
        text=text,
        inline_keyboard_markup=markup)
def updateMessage(bot, chat_id, msg_id, callbackData,name):
    if callbackData in ["onion", "truba"]:
        text = "Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nЭто действие не поможет против вируса!"
    else:
        damage = int(np.random.randn()*20 + 80)
        currHP = explorer.attack_monster(damage=damage, chat_id=chat_id)
        if(chat_id.find("@") != -1):
            text = "Наш вирус обосновался в городе Усть-Камень-Кирка!\n\n{0} нанёс {1} урона!\nСейчас у него {2} HP!\n".format(name,damage,currHP)
        else:    
            text= "Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nТы нанёс {0} урона!\nСейчас у него {1} HP!\n".format(damage,currHP),
    bot.edit_text(chat_id=chat_id, msg_id=msg_id, 
        text=text,
        inline_keyboard_markup=json.dumps(
                          [actions[randrange(7)], actions[randrange(7)]]))
def message_cb(bot, event):
    chat_id = event.data['chat']['chatId']
    if event.text=="/random":
        bot.send_text(chat_id=chat_id, text=str(randrange(101)))
    elif event.text=="/start":
        bot.send_text(chat_id=chat_id, text="Будьте готовы сражаться! Вирус на подходе!")
        explorer.write_chats({'chat_id': chat_id})
    elif event.text == "/create_COVID":
        users = explorer.get_chats_ids()
        explorer.create_monster({"hp":50000000, "endbattle": int(time.time())+12*60*60})
        text = "На карте Лимпопо появился новый вирус! \nУ него зафиксировано {0} HP. Поспеши уничтожить его! \n\n >> /time_to_kill <<".format(explorer.attack_monster(damage=0, chat_id=chat_id))
        send_alerts(users, text)
    elif event.text == "/stats":
        info = explorer.get_dmg(chat_id = chat_id)
        type_chat = "групповой" if chat_id.find("@") > 0 else "личный"
        exp = get_exp(info)
        response = bot.send_text(chat_id=chat_id, text="ИНФОРМАЦИЯ\nСтатус чата: {0}\nУровень чата: {1}\n[{5}] {2}/{3} EXP\nОбщий нанесёный урон вирусу: {4}".format(type_chat, exp['lvl'],exp['last'],exp['aim'] ,info, exp['loader']))
        json_response = response.json()
        explorer.set_stats_id(chat_id=chat_id, stats_id=json_response["msgId"])
    elif event.text == "/time_to_kill":
        kill_id = explorer.get_kill_id(chat_id=chat_id)
        if(kill_id[0]):
            bot.delete_messages(chat_id=chat_id, msg_id=kill_id[0])
        response = bot.send_text(chat_id=chat_id,
                    text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него {0} HP!\n".format(explorer.attack_monster(damage=0, chat_id=chat_id)),
                    inline_keyboard_markup=json.dumps([actions[randrange(7)], actions[randrange(7)]]))
        json_response = response.json()
        explorer.set_kill_id(chat_id= chat_id, kill_id=json_response['msgId'])

def query_cb(bot,event):
    chat_id = event.data['message']['chat']['chatId']
    answer = {
        'desinfect': "Ты продезинфицировал",
        'room': "Ты проветрил комнату",
        'lemon': "Ты выпил чай с лимоном",
        'home': "Ты остался дома",
        'cleaning': "Ты провёл влажную уборку",
        'truba': "Ты прочистил трубу😳",
        'onion': "Ты сделал чесночный киндер😳"
        }
    kill_msg = explorer.get_kill_id(chat_id=chat_id)
    if(time.time() - kill_msg[1] < 46*60*60):
        msg_id = kill_msg[0]
        name = event.data['from']['firstName'] + ' ' + event.data['from']['lastName']
        updateMessage(bot,chat_id,msg_id, event.data['callbackData'], name)
        bot.answer_callback_query(query_id=event.data['queryId'],text=answer[event.data['callbackData']])
        stat_msg = explorer.get_stats_id(chat_id)
        info = explorer.get_dmg(chat_id = chat_id)
        type_chat = "групповой" if chat_id.find("@") > 0 else "личный"
        exp = get_exp(info)
        text = "ИНФОРМАЦИЯ\nСтатус чата: {0}\nУровень чата: {1}\n[{5}] {2}/{3} EXP\nОбщий нанесёный урон вирусу: {4}".format(type_chat, exp['lvl'],exp['last'],exp['aim'] ,info, exp['loader'])
        if(time.time() - stat_msg[1] < 46*60*60):
            msg_id = stat_msg[0]
            updateMessages(bot, chat_id, msg_id, text)
        else:
            bot.delete_messages(chat_id=chat_id, msg_id=kill_msg[0])
            bot.send_text(chat_id=event.from_chat,
                      text=text,
                      inline_keyboard_markup=json.dumps(
                         [actions[randrange(7)], actions[randrange(7)]]))
    else:
        bot.delete_messages(chat_id=chat_id, msg_id=kill_msg[0])
        bot.send_text(chat_id=event.from_chat,
                      text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него {0} HP!\n".format(explorer.attack_monster(damage=0, chat_id=event.data['message']['chat']['chatId'])),
                      inline_keyboard_markup=json.dumps(
                         [actions[randrange(7)], actions[randrange(7)]]))


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=query_cb))
bot.start_polling()
idle.our_idle()
