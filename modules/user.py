from peewee import *
import datetime

class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

class User(BaseModel):
    id = PrimaryKeyField()
    username= CharField(max_length=250, default='', unique=True)
    name = CharField(max_length=250, default='')
    user_id = CharField(max_length=250, default='', unique=True)
    kill_message_id = CharField(max_length=250, default='')
    time_kill_message = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "user"

if __name__ == '__main__':
    db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    db.connect()
    db.create_tables([User])
