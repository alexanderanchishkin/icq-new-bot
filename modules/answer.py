from peewee import *
from modules.clicker import Clicker

class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

class Answer(BaseModel):
    id = PrimaryKeyField()
    text = TextField(default='')
    clicker_id = ForeignKeyField(Clicker, backref='answers')
    likes = IntegerField(default=0)

    class Meta:
        db_table = "answer"

if __name__ == '__main__':
    db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    db.connect()
    Answer.create_table(safe=True)
