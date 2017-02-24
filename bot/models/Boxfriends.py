from datetime import datetime
from peewee import *
from config import BOT_SQLALCHEMY_DATABASE_URI
from bot import logger
import itchat
import time

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


#消息记录
def Add_Message(msg):
    try:
        # id=Wxuser().get_id(msg['FromUserName'])
        id=Wxuser.get(wx_uid=msg['FromUserName'])
        post=Wxpost(body=msg['Text'],timestamp=datetime.now(),wxuser_id=id,sender='普通')
        post.save()
    except BaseException as e:
        logger.debug('Add_Message:')
        logger.debug(e)
#建议记录

def Add_Sugges(msg):
    try:
        id = Wxuser.get(wx_uid=msg['FromUserName'])
        post=Wxpost(body=msg['Text'],timestamp=datetime.utcnow(),wxuser_id=id,sender='建议')
        post.save()
    except BaseException as e:
        logger.debug('Add_Sugges:')
        logger.debug(e)





#获取用户信息
def Get_User_Information(uid,mode):
    try:
        query = Wxuser.get(wx_uid=uid)
        if mode == 'Right':
            return query.right
        elif mode == 'Username':
            if query.remarkname != '':
                return query.remarkname
            else:
                return query.nickname
        elif mode=='id':
            return query.id
    except BaseException as e:
        logger.debug('Get_User_Information:  %s' %mode)
        logger.debug(e)
        if mode=='Right':
            return 1
        elif mode=='Branch':
            return 11
        return '获取失败'


#群发
def Send_msg_all(Text):
    query = db.execute_sql('''SELECT wx_uid FROM Wxuser ''')
    for n in query:
        itchat.send_msg(Text,n[0])
        time.sleep(1)

def Send_msg(id,text):
    user=Wxuser.get(id=id)
    itchat.send_msg(text, user.wx_uid)

def Top_Up_right(id,updata_right):
    try:
        query=Wxuser.get(id=id)
        query.right=int(updata_right)
        query.save()
        return '修改权限 成功'
    except BaseException as e:
        logger.debug('Send_msg_select:')
        logger.debug(e)
        return '没有查询到ID'

