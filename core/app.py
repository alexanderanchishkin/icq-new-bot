from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = "001.3146970085.4148216257:752501352"

bot = Bot(token=TOKEN)


def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat, text=event.text)


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()
