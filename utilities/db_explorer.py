from peewee import *
from models.users import Users

SQL_MODE = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,' \
           'NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION'

class DBExplorer:
    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        pass

    def __init__(self):
        self.db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432, SQL_MODE=SQL_MODE)
        
    def write(self, args):
        self.db.connect()
        user = Users.insert(**args)
        user.execute()

    def update(self, args, search_id=1):
        self.db.connect()
        user = Users.update(**args).where(Users.icq_id == search_id)
        user.execute()