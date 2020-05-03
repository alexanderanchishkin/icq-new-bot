from random import randrange

from bot.bot import Bot
from bot.handler import MessageHandler

TOKEN = "001.3146970085.4148216257:752501352"
# TOKEN = "001.2407941028.1045918646:752505142" мой токен


bot = Bot(token=TOKEN)
db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
db.connect()


def message_cb(bot, event):
    if event.text=="/random":
        bot.send_text(chat_id=event.from_chat, text=str(randrange(101)))
    elif event.text=="/start":
        start_message = "Привет, {0} {1}. Я знаю про тебя все: \n{2}".format(
            event.data['from']['firstName'],
            event.data['from']['lastName'],
            event.data)
        bot.send_text(chat_id=event.from_chat, text=start_message)
    elif event.text == "/advice":
        bot.send_text(chat_id=event.from_chat, text="Напиши свой совет для других")
        setState(event.from_id, "advice")
    elif event.text == "/getTopAdvice":
        bot.send_text(chat_id=event.from_chat, text="ТОП-5 СОВЕТОВ ПОЛЬЗОВАТЕЛЕЙ\n\n1. Кушац\n2. Не пить\n3. Спать\n4. Работать\n5. Кушац")
    else:
        if(getState(event.from_id) == "advice"):
            bot.send_text(chat_id=event.from_chat, text="Спасибо за твой совет :)\nЯ его записал")
            setState(event.from_id, "")
            # запись совета в бд
        bot.send_text(chat_id=event.from_chat, text=event.text)

def setState(chat_id, state):
    row = State(
        chat_id = chat_id,
        state = state
    )
    row.save()

def getState(chat_id):
    return State.get(State.chat_id == chat_id)

bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.start_polling()
bot.idle()
