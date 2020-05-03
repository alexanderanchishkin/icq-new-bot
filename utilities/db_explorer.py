from peewee import *
from models.users import Users
from models.state import State
from models.advices import Advices

class DBExplorer:
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def __init__(self):
        self.db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

    def write_users(self, args):
        self.db.connect()
        user = Users.insert(**args)
        user.execute()

    def update_users(self, args, search_id=1):
        self.db.connect()
        user = Users.update(**args).where(Users.user_id == search_id)
        user.execute()

    def write_advices(self, args):
        self.db.connect()
        advices = Advices.insert(**args)
        Advices.execute()

    def update_advices(self, args, search_id=1):
        self.db.connect()
        advices = Advices.update(**args).where(Advices.user_id == search_id)
        advices.execute()

    def write_states(self, args):
        self.db.connect()
        states = State.insert(**args)
        states.execute()

    def update_states(self, args, search_id=1):
        self.db.connect()
        states = State.update(**args).where(State.user_id == search_id)
        states.execute()

    def get_states(self, chat_id):
        return State.get(State.user_id == chat_id)
