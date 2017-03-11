from datetime import datetime
from bot import logger
import itchat
import time
from app.models import Wxuser,Wxpost


#消息记录
def Add_Message(msg):
    try:
        id=Wxuser().get_name(msg['FromUserName'])
        post=Wxpost(body=msg['Text'],timestamp=datetime.now(),wxuser_id=id,sender='普通')
        post.save()
    except BaseException as e:
        logger.debug('Add_Message:')
        logger.debug(e)
#建议记录

def Add_Sugges(msg,**kwargs):
    try:
        id = Wxuser().get_name(kwargs['FromUserName'])
        post=Wxpost(body=msg,timestamp=datetime.utcnow(),wxuser_id=id,sender='建议')
        post.save()
    except BaseException as e:
        logger.debug('Add_Sugges:')
        logger.debug(e)

def return_user(id):
    q=Wxuser.query.filter_by(id=id).first()
    return q



#获取用户信息
def Get_User_Information(uid,mode):
    try:
        query = Wxuser().get(uid)
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
    query = Wxuser.query.all()
    for n in query:
        itchat.send_msg(Text,n.wx_uid)
        time.sleep(1)

def Send_msg(id,text):
    user=Wxuser.query.filter_by(id=id).first()
    itchat.send_msg(text, user.wx_uid)

def Top_Up_right(id,updata_right):
    try:
        query =Wxuser.query.filter_by(id=id).first()
        query.right=int(updata_right)
        query.save()
        return '修改权限 成功'
    except BaseException as e:
        logger.debug('Send_msg_select:')
        logger.debug(e)
        return '没有查询到ID'

