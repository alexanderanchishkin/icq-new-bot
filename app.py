import os

from random import randrange

from utilities.db_explorer import *
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler

import json

# 001.3146970085.4148216257:752501352 main token
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
        start_message = "Привет, {0} {1}. Я знаю про тебя все: \n{2}".format(
            event.data['from']['firstName'],
            event.data['from']['lastName'],
            event.data)
        bot.send_text(chat_id=event.from_chat, text=start_message)
    elif event.text == "/time_to_kill":
        bot.send_text(chat_id=event.from_chat, text="Наш вирус обосновался в городе Усть-Камень-Кирка!\n\nСейчас у него 50000000 HP!\n", 
        inline_keyboard_markup = json.dumps([[{"text": "Произвести дезинфекцию", "callbackData": "desinfect"}],[{"text": "Прочистить трубу", "callbackData": "clear"}]]))
    else:
        bot.send_text(chat_id=event.from_chat, text=event.text)

def query_cb(bot,event):
    if event.data.callbackData == "desinfect":
        bot.send_text(chat_id= event.from_chat, text= "Молодец")
    # bot.answer_callback_query(query_id=event.data.queryId,text="Ты продизенфицировал", show_alert=True)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=query_cb))
bot.start_polling()
bot.idle()
