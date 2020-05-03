from peewee import *
import datetime
from modules.answer import Answer

class BaseModel(Model):
    class Meta:
        database = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

class UserAnswer(BaseModel):
    id = PrimaryKeyField()
    user_id = CharField(max_length=250, default='')
    answer_id = ForeignKeyField(Answer, backref='users')
    created_at = DateTimeField(default=datetime.datetime.now())

    class Meta:
        db_table = "useranswer"

if __name__ == '__main__':
    db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    db.connect()
    UserAnswer.create_table(safe=True)
