# -*- coding: utf-8 -*-
from bot.models.view import *
from itchat.content import *
from bot import logger
from bot.models.Boxfriends import Wxuser
from threading import Thread

#功能状态读取
global Functional_status
Functional_status=Update_function_status()

#权限设置
RIGHT={
    0:{
        '错误权限':'错误权限'
    },
    1:{
        '积分':'Get_vip_integral',
        '建议':'Add_suggest',
        '设置专柜':'Set_zgcode',
        'ID':'Get_my_id',
        'id':'Get_my_id',
    },
    2:{
        '积分':'Get_vip_integral',
        '建议':'Add_suggest',
        '销售报表':"Sale_table",
        '销售':"Sale_today",
        '专柜销售':'Sale_Brand_All',
        '专柜详细': 'Sale_Brand_Table',
        '设置专柜':'Set_zgcode',
        'ID': 'Get_my_id',
        'id': 'Get_my_id',
    },
    3: {
        '积分':'Get_vip_integral',
        '建议':'Add_suggest',
        '对账单': 'Send_bill_balance_teble',
        '销售报表':"Sale_table",
        '销售':"Sale_today",
        '专柜销售':'Sale_Brand_All',
        '专柜详细': 'Sale_Brand_Table',
        'ID': 'Get_my_id',
        'id': 'Get_my_id',
    },
    4: {
        '积分':'Get_vip_integral',
        '建议':'Add_suggest',
        '对账单': 'Send_bill_balance_teble',
        '销售报表':"Sale_table",
        '销售':"Sale_today",
        '专柜销售': 'Sale_Brand_All',
        '专柜详细': 'Sale_Brand_Table',
        '群发':'Send_msg_all',
        '权限':'Top_Up_right',
        '更新':'update_zg',
        'ID': 'Get_my_id',
        'id': 'Get_my_id',
    }
}

@itchat.msg_register(TEXT)
def text_reply(msg):
    logger.debug('sendtext:%s'%msg)
    try:
        text=msg['Text'].split(' ')[0]
        if text in Functional_status:
            if Functional_status[RIGHT[4][text]]:
                func = eval(RIGHT[Get_right(msg['FromUserName'])][text])
                Add_Message(msg)  # 日志记录
                return func(msg['Text'], FromUserName=msg['FromUserName'])
            else:
                return '%s 停用ing' % text
        func = eval(RIGHT[Get_right(msg['FromUserName'])][text])
        return func(msg['Text'], FromUserName=msg['FromUserName'])

    except KeyError as e:
        logger.warning(e)
        if Functional_status['Reboton']:
            return Tuling_box(msg['Text'],FromUserName=msg['FromUserName'])


#收到好友邀请自动添加好友
@itchat.msg_register(FRIENDS)
def add_friend(msg):
    if not Functional_status['Add_friend']:
        return 'True'
    itchat.add_friend(**msg['Text'])
    wx_uin = re.findall(r'<msg fromusername="([\S\s]+?)" ',str(msg))[0]
    try:
        wxuser = Wxuser.query.filter_by(wx_uin=wx_uin).first()
        if wxuser:
            wxuser.nickname = msg['RecommendInfo']['NickName']
            wxuser.wx_uid = msg['RecommendInfo']['UserName']
            wxuser.save()
        else:
            wxuser = Wxuser(wx_uin=wx_uin,
                            nickname = msg['RecommendInfo']['NickName'],
                            wx_uid=msg['RecommendInfo']['UserName'])
            wxuser.save()
    except:
        wxuser.rollback()
    try:
        itchat.send_msg('Nice to meet you! \nID：%s'% wxuser.id, msg['RecommendInfo']['UserName'])
    except:
        itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])


@itchat.msg_register(SYSTEM)
def get_uin(msg):
    if msg['SystemInfo'] != 'uins': return
    if len(msg['Text']) == 0: return
    try:
        ins = itchat.instanceList[0]
        fullContact = ins.memberList
        # 更新用户数据到数据库
        print('****  Wx_uin  ****')
        if fullContact:
            for row in fullContact:
                print(row['Uin'])
                if row['Uin']!=0:
                    try:
                        wxuser = Wxuser.query.filter_by(wx_uin=row['Uin']).first()
                        if wxuser:
                            wxuser.nickname = row['NickName']
                            wxuser.remarkname = row['RemarkName']
                            wxuser.wx_uid = row['UserName']
                            wxuser.save()
                        else:
                            wxuser = Wxuser(wx_uin=row['Uin'],
                                            nickname=row['NickName'],
                                            remarkname=row['RemarkName'],
                                            wx_uid=row['UserName'])
                            wxuser.save()
                    except:
                        wxuser.rollback()
    except BaseException as e:
        logger.debug(e)

#UPD 通讯
def UDP():
    global Functional_status
    import socket
    import os
    while True:
        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # 绑定端口:
            ss.bind(('127.0.0.1', 9999))
            logger.debug('Bind UDP on 9999...')
            while True:
                data, addr = ss.recvfrom(1024)
                text = data.decode('utf-8')
                if text == 'pid':
                    pid = '%s' % os.getpid()
                    ss.sendto(pid.encode(), addr)
                elif 'name' in text:
                    setrickname(text.split(' ')[1],text.split(' ')[2])
                elif 'Update' in text:
                    Functional_status = Update_function_status()
                else:
                    logger.debug(text)
                    id = text.split()[0]
                    sendstr = re.findall(r'\(([\S\s]+)\)', text)
                    if sendstr[0]:
                        send_msg(id, sendstr[0])
        except BaseException as e:
            logger.debug(e)

def ec():
    # 机器人退出 发送短信
    if Functional_status['OnSendalarmMsg']:
        Send_Sms_msg(Functional_status['adminphone'])

thr = Thread(target=UDP, args=[])
thr.setDaemon(True)
thr.start()
itchat.auto_login(False,exitCallback=ec)#暂存登录状态
itchat.run()
