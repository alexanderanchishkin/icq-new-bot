from peewee import *
from modules.clicker import Clicker
from modules.answer import Answer
from modules.useranswer import UserAnswer
from modules.user import User

class DBExplorer:
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def __init__(self):
        self.db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

    def write_clicker(self, args):
        self.db.connect()
        Clicker.insert(**args).execute()

    def write_answer(self, args):
        self.db.connect()
        Answer.insert(**args).execute()

    def write_useranswer(self, args):
        self.db.connect()
        UserAnswer.insert(**args).execute()

    def write_user(self, args):
        self.db.connect()
        User.insert(**args).execute()



