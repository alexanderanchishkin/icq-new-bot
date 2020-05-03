from peewee import *
from users import Users

class BaseModel(Model):

    class Meta:
        database = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

class Advices(BaseModel):
    id = PrimaryKeyField(null=False)
    advice = TextField(default='')
    user_id = ForeignKeyField(Users, backref="advices")

    class Meta:
        db_table = "advices"


#if __name__ == '__main__':
    # db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
    #                          password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
    #                          host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    # db.connect()
    # Advices.create_table(safe=True)
