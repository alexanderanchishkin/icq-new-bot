from random import randrange

from utilities.db_explorer import *
from bot.bot import Bot
from bot.handler import MessageHandler


TOKEN = "001.3146970085.4148216257:752501352"


bot = Bot(token=TOKEN)
explorer = DBExplorer()
db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
db.connect()

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
        inlineKeyboardMarkup = [[{text: "Произвести дезинфекцию", callbackData: "desinfect"}, {text: "Прочистить трубу", callbackData: "clear"}]])
    else:
        if(explorer.get_states(event.from_chat) == "advice"):
            bot.send_text(chat_id=event.from_chat, text="Спасибо за твой совет :)\nЯ его записал")
            explorer.update_states({"user_id": event.from_chat, "state": ""})
            # запись совета в бд
        bot.send_text(chat_id=event.from_chat, text=event.text)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()