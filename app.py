import os
import time

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

def send_alerts(users, text):
    for user in users:
        bot.send_text(chat_id=user, text=text)
def updateMessage(bot, chat_id, msg_id):
    damage = randrange(101)
    currHP = explorer.attack_monster(damage=damage)
    bot.edit_text(chat_id=chat_id, msg_id=msg_id, 
    text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nТы нанёс {0} урона!\nСейчас у него {1} HP!\n".format(damage,currHP),
    inline_keyboard_markup=json.dumps(
                          [[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
                           [{"text": "Прочистить трубу", "callbackData": "clear"}]]))
def message_cb(bot, event):
    if event.text=="/random":
        bot.send_text(chat_id=event.from_chat, text=str(randrange(101)))
    elif event.text=="/start":
        bot.send_text(chat_id=event.from_chat, text="Registration in process")
        try:
            explorer.write_user({'username':event.data['from'].get('nick', ''),
                                'name': event.data['from'].get('firstName', '')+' '+event.data['from'].get('lastName', ''),
                                'user_id': event.data['from']['userId'], 'kill_message_id':'',
                                'lvl':1, 'total_dmg':100})
        except:
            print('ОШИБКА!')
            import traceback
            traceback.print_exc()
            print('mes')
    elif event.text == "/create_COVID":
        users = explorer.get_user_ids()
        explorer.create_monster({"hp":50000000, "endbattle": int(time.time())+12*60*60})
        text = "На карте Черноруссии появился новый вирус! \nУ него зафиксировано {0} HP. Поспеши уничтожить его! \n\n >> /time_to_kill <<".format(explorer.attack_monster(damage=0, user_id=event.data['message']['chat']['chatId']))
        send_alerts(users, text)
    elif event.text == "/time_to_kill":
        response = bot.send_text(chat_id=event.from_chat,
                      text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него {0} HP!\n".format(explorer.attack_monster(damage=0)),
                      inline_keyboard_markup=json.dumps(
                          [[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
                           [{"text": "Прочистить трубу", "callbackData": "clear"}]]))
        json_response = response.json()
        explorer.set_kill_id(user_id= event.from_chat, kill_id=json_response['msgId'])
    else:
        bot.send_text(chat_id=event.from_chat, text=event.text)

def query_cb(bot,event):
    answer = {'desinfect': "Ты продезинфицировал"}
    kill_msg = explorer.get_kill_id(user_id= event.data['from']['userId'])
    if(time.time() - kill_msg[1] < 48*60*60):
        msg_id = kill_msg[0]
        updateMessage(bot,event.data['message']['chat']['chatId'],msg_id)
        bot.answer_callback_query(query_id=event.data['queryId'],text=answer[event.data['callbackData']])
    else: 
        bot.send_text(chat_id=event.from_chat,
                      text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него {0} HP!\n".format(explorer.attack_monster(damage=0)),
                      inline_keyboard_markup=json.dumps(
                          [[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
                           [{"text": "Прочистить трубу", "callbackData": "clear"}]]))


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=query_cb))
bot.start_polling()
idle.our_idle()
