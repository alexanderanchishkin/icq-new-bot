from peewee import *
import time

from modules.monster import Monster
from modules.chats import Chats

class DBExplorer:
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def __init__(self):
        self.db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
        self.db.connect()

    def write_chats(self, args):
        Chats.insert(**args).on_conflict_ignore().execute()

    def get_chats_ids(self):
        return [chat.chat_id for chat in Chats.select(Chats.chat_id)]

    def create_monster(self, args):
        try:
            self.kill_monster()
        except:
            pass
        Monster.insert(**args).execute()

    def attack_monster(self, damage, chat_id):
        monster = Monster.get(Monster.hp != None)
        chat = Chats.get(Chats.chat_id == chat_id)
        monster.hp-=damage
        chat.total_dmg += damage
        rem_hp = monster.hp
        monster.save()
        chat.save()
        return rem_hp

    def kill_monster(self):
        Monster.get(Monster.hp != None).delete_instance()

    def get_kill_id(self, chat_id):
        chat = Chats.get(Chats.chat_id==chat_id)
        return chat.kill_message_id, chat.time_kill_message

    def set_kill_id(self, chat_id, kill_id, time_kill=time.time()):
        chat = Chats.get(Chats.chat_id==chat_id)
        chat.kill_message_id = kill_id
        chat.time_kill_message = time_kill
        chat.save()

    def get_lvl(self, chat_id):
        chat = Chats.get(Chats.chat_id==chat_id)
        return {'lvl': chat.lvl, 'total_dmg': chat.total_dmg}