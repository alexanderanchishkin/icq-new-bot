from random import randrange

from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = "001.3146970085.4148216257:752501352"


bot = Bot(token=TOKEN)


def message_cb(bot, event):
    if event.text=="/random":
        bot.send_text(chat_id=event.from_chat, text=str(randrange(101)))
    elif event.text=="/start":
        start_message = "Привет, {0} {1}. Я знаю про тебя все: \n{2}".format(
            event.data['from']['firstName'],
            event.data['from']['lastName'],
            event.data)
        bot.send_text(chat_id=event.from_chat, text=start_message)
    else:
        bot.send_text(chat_id=event.from_chat, text=event.text)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()
