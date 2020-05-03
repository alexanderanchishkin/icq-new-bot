from peewee import *

class BaseModel(Model):

    class Meta:
        database = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                                password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                                host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)

class Users(BaseModel):
    id = PrimaryKeyField(null=False)
    username = CharField(max_length=250, default='')
    name = CharField(max_length=250, default='')
    icq_id = CharField(max_length=250, default = '')

    class Meta:
        db_table = "users"


if __name__ == '__main__':
    # db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
    #                         password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
    #                         host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    # db.connect()
    # Users.create_table(safe=True)
    db = PostgresqlDatabase('dc9gn4kbsdd0mi', user='onpzldzoogstwe',
                             password='5b444a910f1acd6eedb48fd391bcb5c891e53eba17ee1401a513aba0e783e12e',
                             host='ec2-3-211-48-92.compute-1.amazonaws.com', port=5432)
    db.connect()
    print(db)