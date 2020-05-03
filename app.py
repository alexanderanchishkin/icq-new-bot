import os

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

def message_cb(bot, event):
    if event.text=="/random":
        bot.send_text(chat_id=event.from_chat, text=str(randrange(101)))
    elif event.text=="/start":
        bot.send_text(chat_id=event.from_chat, text="Registration in process")
        try:
            explorer.write_user({'username':event.data['from']['nick'],
                                'name': event.data['from']['firstName']+' '+event.data['from']['lastName'],
                                'user_id': event.data['from']['userId']})
        except:
            print('ОШИБКА!')
            import traceback
            traceback.print_exc()
            print('mes')
    elif event.text == "/time_to_kill":
        bot.send_text(chat_id=event.from_chat,
                      text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него 50000000 HP!\n",
                      inline_keyboard_markup=json.dumps(
                          [[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],
                           [{"text": "Прочистить трубу", "callbackData": "clear"}]]))
    else:
        bot.send_text(chat_id=event.from_chat, text=event.text)

def query_cb(bot,event):
    answer = {'desinfect': "Ты продезинфицировал"}
    bot.answer_callback_query(query_id=event.data['queryId'],text=answer[event.data['callbackData']], show_alert=True)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=query_cb))
bot.start_polling()
idle.our_idle()
