
from peewee import *
from config import BOT_SQLALCHEMY_DATABASE_URI


db = SqliteDatabase(BOT_SQLALCHEMY_DATABASE_URI)

class BaseModel(Model):
    class Meta:
        database = db


class Wxuser(BaseModel):
    wx_uin=CharField(unique = True,index=True)
    wx_uid=CharField(default='')
    nickname=CharField(default='')
    remarkname=CharField(default='')
    right = IntegerField(default=1)

class Wxpost(BaseModel):
    sender=CharField(default='')
    body = CharField(default='')
    timestamp = DateTimeField()
    wxuser_id = ForeignKeyField(Wxuser, related_name='Messages')

