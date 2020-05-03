import os

from random import randrange

from utilities import idle
from utilities.db_explorer import *
from bot.bot import Bot
from bot.handler import MessageHandler

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
db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                        password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                        host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
db.connect()
commands = ["/random", "/start", "/advice", "/get_top_advices", "get_next_advice"]


def message_cb(bot, event):
    bot.answer_callback_query(query_id="desinfect", text="Ты продизенфицировал", show_alert=True)

    if event.text == "/random":
        bot.send_text(chat_id=event.from_chat, text=str(randrange(101)))
    elif event.text=="/start":
        bot.send_text(chat_id=event.from_chat, text="Registration in process")
        try:
            explorer.write_user({'username':event.data['from']['nick'],
                                'name': event.data['from']['firstName']+' '+event.data['from']['lastName'],
                                'user_id': event.data['from']['userId']})
        except:
            print('mes')
    elif event.text == "/time_to_kill":
        bot.send_text(chat_id=event.from_chat,
                      text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него 50000000 HP!\n",
                      inline_keyboard_markup=json.dumps(
                          [[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
                           [{"text": "Прочистить трубу", "callbackData": "clear"}]]))
    else:
        bot.send_text(chat_id=event.from_chat, text=event.text)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
idle.our_idle()
