from peewee import *
from modules.clicker import Clicker
from modules.answer import Answer
from modules.useranswer import UserAnswer
from modules.user import User
from modules.monster import Monster


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

    def write_clicker(self, args):
        Clicker.insert(**args).execute()

    def write_answer(self, args):
        Answer.insert(**args).execute()

    def write_useranswer(self, args):
        UserAnswer.insert(**args).execute()

    def write_user(self, args):
        User.insert(**args).on_conflict_ignore().execute()

    def get_user_ids(self):
        return [user.user_id for user in User.select(User.user_id)]

    def create_monster(self, args):
        try:
            self.kill_monster()
        except:
            pass
        Monster.insert(**args).execute()

    def attack_monster(self, damage):
        monster = Monster.get(Monster.hp != None)
        monster.hp-=damage
        rem_hp = monster.hp
        monster.save()
        return rem_hp

    def kill_monster(self):
        Monster.get(Monster.hp != None).delete_instance()

    def get_kill_id(self, user_id):
        user = User.get(User.user_id==user_id)
        return user.kill_message_id

    def set_kill_id(self, user_id, kill_id):
        user = User.get(User.user_id==user_id)
        user.kill_message_id = kill_id
        user.save()