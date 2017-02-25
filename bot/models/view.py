import datetime
import time
import re
import itchat
from threading import Thread

from bot import logger
from bot.models import wumis
from bot.models import Boxfriends
from bot.models import wudebit
from bot.models import _Fcunction
from bot.models import Tuling
from bot.models import Images
from bot.models.alidayu import AlibabaAliqinFcSmsNumSendRequest



def Tuling_box(text,**kwargs):return Tuling.get_response(text,**kwargs)#图灵机器人
def Add_Message(msg):Boxfriends.Add_Message(msg)#日志记录
def Add_suggest(msg,**kwargs):Boxfriends.Add_Sugges(msg)#建议
def Get_right(uid):return Boxfriends.Get_User_Information(uid,'Right')#查询用户权限
def Get_username(uid):return Boxfriends.Get_User_Information(uid,'Username')#获得用户名字



def Send_Sms_msg():
    req = AlibabaAliqinFcSmsNumSendRequest('23578698', 'a74a15404e8b4e2780dde859c7efd096')
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = "机器人"
    req.sms_param = ""
    req.rec_num = "13541106254,13518204382"
    req.sms_template_code = "SMS_35770009"
    resp = req.getResponse()
    logger.info(resp)

#查询积分
def Get_vip_integral(text,**kwargs):
    try:
        text = text.split(' ')
        if len(text) == 2:
            code = text[1]
            p = re.compile('[A-Za-z]')
            if len(code) == 6 or len(code) == 8:
                if not p.match(code):
                    ret = wudebit.Select_vip_integral(code)
                    return ret
            elif len(code) == 11:
                if not p.match(code):
                    ret = wudebit.Select_vip_code(code)
                    return ret
            return '无该卡号'
        else:
            return 'error:指令错误\n积分 [卡号或者电话号码]\n例：积分 123456\n返回数据 123456现有积分'
    except IndexError as e:
        logger.debug('Get_vip_integral 指令错误')
        return ('注意空格')

#销售报表
def Sale_table(text,**kwargs):
    try:
        text = text.split(' ')
        if len(text) == 1:
            return 'error:参数设置错误\n销售报表 [楼层] (开始日期) (结束日期)\n例：销售报表 1 12-1 12-5\n返回数据为1楼，12月1日-5日 销售报表'
        # 2个参数
        if int(text[1]) > 5 or int(text[1]) == 0:
            return 'error:楼层信息设置错误\n 设置范围(1-4) 4表示所有楼层'
        if len(text) == 2:
            if int(text[1]) == 4:
                return wumis.Get_sell(mode=1)
            return wumis.Get_sell(depart=int(text[1]), mode=1)
            # 3个参数
        try:
            if len(text) == 3:
                try:
                    datemin = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()  # 带有年格式
                    datemin = datemin.strftime('%m-%d-%Y')
                    if int(text[1]) == 4:
                        return wumis.Get_sell(datemin, datemin, mode=1)
                    return wumis.Get_sell(datemin, datemin, depart=int(text[1]), mode=1)
                except:
                    datetime.datetime.strptime(text[2], "%m-%d").date()  # 没有年格式
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[2], year)
                    if int(text[1]) == 4:
                        return wumis.Get_sell(datemin, datemin, mode=1)
                    return wumis.Get_sell(datemin, datemin, depart=int(text[1]), mode=1)
            else:
                try:
                    datemin = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()  # 带有年格式
                    datemin = datemin.strftime('%m-%d-%Y')
                    datemax = datetime.datetime.strptime(text[3], "%Y-%m-%d").date()
                    datemax = datemax.strftime('%m-%d-%Y')
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    if int(text[1]) == 4:
                        return wumis.Get_sell(datemin, datemax, mode=1)
                    return wumis.Get_sell(datemin, datemax, depart=int(text[1]), mode=1)
                except ValueError as e:
                    datetime.datetime.strptime(text[2], "%m-%d").date()  # 没有年格式
                    datetime.datetime.strptime(text[3], "%m-%d").date()
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[2], year)
                    datemax = '%s-%s' % (text[3], year)
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    if int(text[1]) == 4:
                        return wumis.Get_sell(datemin, datemax, mode=1)
                    return wumis.Get_sell(datemin, datemax, depart=int(text[1]), mode=1)
        except:
            return 'error:时间设置错误 or 时间差大于30天\n销售报表 [楼层] [开始日期] [结束日期]\n例：销售报表 1 12-1 12-5\n返回数据为1楼，12月1日-5日 销售报表'  # 销售报表  #销售   小收
    except IndexError as e:
        logger.debug('Sale_table 指令错误')
        return ('注意空格')

#销售总计
def Sale_today(text,**kwargs):
    try:
        text = text.split(' ')
        if len(text) > 3:
            return 'error:参数设置\n销售 [开始日期] [结束日期]\n例：销售 5-1 6-10\n返回数据为1、2、3楼5月1日-6月10日 销售总计'
        if len(text) == 1:
            return wumis.Get_sell()
        try:
            if len(text) == 2:
                try:
                    datemin = datetime.datetime.strptime(text[1], "%Y-%m-%d").date()  # 年参数
                    datemin = datemin.strftime('%m-%d-%Y')
                    return wumis.Get_sell(datemin, datemin)
                except:
                    datetime.datetime.strptime(text[1], "%m-%d").date()  # 无年参数
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[1], year)
                    return wumis.Get_sell(datemin, datemin)
            if len(text) == 3:
                try:
                    datemin = datetime.datetime.strptime(text[1], "%Y-%m-%d").date()  # 带有年格式
                    datemin = datemin.strftime('%m-%d-%Y')
                    datemax = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()
                    datemax = datemax.strftime('%m-%d-%Y')
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_sell(datemin, datemax)
                except:
                    datetime.datetime.strptime(text[1], "%m-%d").date()  # 没有年格式
                    datetime.datetime.strptime(text[2], "%m-%d").date()
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[1], year)
                    datemax = '%s-%s' % (text[2], year)
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_sell(datemin, datemax)
        except:
            return 'error:时间设置错误 or 时间差大于30天\n销售 [开始日期] [结束日期]\n例：销售 5-1 6-10\n返回数据为1、2、3楼5月1日-6月10日 销售总计'
    except IndexError as e:
        logger.debug('Sale_today 指令错误')
        return ('注意空格')

#专柜销售总计
def Sale_Brand_All(text,**kwargs):
    try:
        text = text.split(' ')
        if len(text) > 4:
            return 'error:时间设置错误 or 时间差大于30天\n专柜销售 [专柜代码] [开始日期] [结束日期]\n例：专柜销售 110001 5-1 6-10\n返回数据为 110001专柜 5月1日-6月10日 销售详细'
        if len(text) == 2:
            return wumis.Get_zg_sell(zgcode=text[1],mode=1)
        try:
            zgcode=text[1]
            if len(text) == 3:
                try:
                    datemin = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()  # 年参数
                    datemin = datemin.strftime('%m-%d-%Y')
                    return wumis.Get_zg_sell(zgcode,datemin, datemin,mode=1)
                except:
                    datetime.datetime.strptime(text[2], "%m-%d").date()  # 无年参数
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[2], year)
                    return wumis.Get_zg_sell(zgcode,datemin, datemin,mode=1)
            if len(text) == 4:
                try:
                    datemin = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()  # 带有年格式
                    datemax = datetime.datetime.strptime(text[3], "%Y-%m-%d").date()
                    datemin = datemin.strftime('%m-%d-%Y')
                    datemax = datemax.strftime('%m-%d-%Y')
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_zg_sell(zgcode,datemin, datemax,mode=1)
                except:
                    datetime.datetime.strptime(text[2], "%m-%d").date()  # 没有年格式
                    datetime.datetime.strptime(text[3], "%m-%d").date()
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[2], year)
                    datemax = '%s-%s' % (text[3], year)
                    if _Fcunction.Com_Date_Poor(datemin,datemax)>31 or _Fcunction.Com_Date_Poor(datemin,datemax)<=-1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_zg_sell(zgcode,datemin, datemax,mode=1)
        except:
            return 'error:时间设置错误 or 时间差大于30天\n专柜销售 [专柜代码] [开始日期] [结束日期]\n例：专柜销售 110001 5-1 6-10\n返回数据为 110001专柜 5月1日-6月10日 销售详细'
    except IndexError as e:
        logger.debug('Sale_brand 指令错误')
        logger.debug(e)
        return ('注意空格')

#查询专柜详细
def Sale_Brand_Table(text, **kwargs):
    msg=text
    try:
        text = text.split(' ')
        if len(text) > 4:
            return 'error:时间设置错误 or 时间差大于30天\n专柜报表 [专柜代码] [开始日期] [结束日期]\n例：专柜销售 110001 5-1 6-10\n返回数据为 110001专柜 5月1日-6月10日 销售详细'
        if len(text) == 2:
            return Sale_Brand_All(msg)
        if len(text)==3:
            return Sale_Brand_All(msg)
        try:
            zgcode = text[1]
            if len(text) == 4:
                try:
                    datemin = datetime.datetime.strptime(text[2], "%Y-%m-%d").date()  # 带有年格式
                    datemax = datetime.datetime.strptime(text[3], "%Y-%m-%d").date()
                    datemin = datemin.strftime('%m-%d-%Y')
                    datemax = datemax.strftime('%m-%d-%Y')
                    if _Fcunction.Com_Date_Poor(datemin, datemax) > 31 or _Fcunction.Com_Date_Poor(datemin,
                                                                                                   datemax) <= -1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_zg_sell(zgcode, datemin, datemax, mode=0)
                except:
                    datetime.datetime.strptime(text[2], "%m-%d").date()  # 没有年格式
                    datetime.datetime.strptime(text[3], "%m-%d").date()
                    year = time.strftime("%Y",time.localtime(time.time()))
                    datemin = '%s-%s' % (text[2], year)
                    datemax = '%s-%s' % (text[3], year)
                    if _Fcunction.Com_Date_Poor(datemin, datemax) > 31 or _Fcunction.Com_Date_Poor(datemin,
                                                                                                   datemax) <= -1:
                        return '时间设置错误 or 时间差大于30天'
                    return wumis.Get_zg_sell(zgcode, datemin, datemax, mode=0)
        except IndexError as e:
            return 'error:时间设置错误 or 时间差大于30天\n专柜报表 [专柜代码] [开始日期] [结束日期]\n例：专柜销售 110001 5-1 6-10\n返回数据为 110001专柜 5月1日-6月10日 销售详细'
    except IndexError as e:
        logger.debug('Sale_Brand_Table 指令错误')
        logger.debug(e)
        return ('注意空格')





# 发送消息 family=群发楼层
def Send_msg_all(msg, **kwargs):
    try:
        text = msg.split(' ')
        if len(text) == 1:
            return 'error:指令错误'
        #sendname = Get_username(kwargs['FromUserName'])
        sendstr = re.findall(r'\(([\S\s]+)\)', msg)
        if sendstr:
            thr = Thread(target=Boxfriends.Send_msg_all, args=[sendstr])
            thr.start()
    except IndexError as e:
        logger.debug('Send_msg_all 指令错误')
        logger.debug(e)
        return ('注意空格')

def send_msg(id,text):
    Boxfriends.Send_msg(id,text)


def setrickname(id,name):
    user=Boxfriends.Wxuser.get(id=int(id))
    logger.debug(user.wx_uid)
    itchat.set_alias(user.wx_uid,name)

#====财务使用
#发送对账单
def Send_bill_balance_teble(text,**kwargs):
    lzgs=['210001','210002','210003','310039']
    try:
        if Get_right(kwargs['FromUserName']) == 1:
            return '输入错误，请重新输入'
            #未开启导购查询模式
            # 导购查询
            zgcode = Get_Branch(kwargs['FromUserName'])
            if zgcode<'11':
                return '请先设置专柜代码,不清楚,请询问楼层主管'
            if int(time.strftime("%d",time.localtime(time.time())))<7 or int(time.strftime("%d",time.localtime(time.time())))>9:
                return '对账日期为7号到9号'
            #===
            if not zgcode in lzgs:
                datemax = datetime.datetime.strptime('%s-%s-25' % (time.strftime("%Y",time.localtime(time.time())), int(time.strftime("%m",time.localtime(time.time()))) - 1),
                                                     "%Y-%m-%d").date()  # 带有年格式
                datemin = datemax - datetime.timedelta(seconds=60 * 60 * 24 * 30)
                datemax = datemax.strftime('%Y-%m-25')
                datemin = datemin.strftime('%Y-%m-26')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    return '@img@%s' % (
                    Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName']))
                else:
                    return ret
            else:
                #26-10
                datemax = datetime.datetime.strptime('%s-%s-10' % (time.strftime("%Y",time.localtime(time.time())), int(time.strftime("%m",time.localtime(time.time()))) - 1),
                                                     "%Y-%m-%d").date()  # 带有年格式
                datemin = datemax - datetime.timedelta(seconds=60 * 60 * 24 * 30)
                datemax = datemax.strftime('%Y-%m-10')
                datemin = datemin.strftime('%Y-%m-26')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    retpath=Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName'])
                    itchat.send('@img@%s' % (retpath), kwargs['FromUserName'])
                #10-25
                datemax = datetime.datetime.strptime('%s-%s-10' % (time.strftime("%Y",time.localtime(time.time())), int(time.strftime("%m",time.localtime(time.time()))) - 1),
                                                     "%Y-%m-%d").date()  # 带有年格式
                #datemin = datemax - datetime.timedelta(seconds=60 * 60 * 24 * 30)
                datemin = datemax.strftime('%Y-%m-11')
                datemax = datemax.strftime('%Y-%m-25')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    retpath=Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName'])
                    itchat.send('@img@%s' % (retpath), kwargs['FromUserName'])
        else:
            text = text.split(' ')
            if len(text) != 3:
                return '参数设置错误 注意空格'
            zgcode = text[1]
            if not _Fcunction.Judge_zgcode(zgcode):
                return '专柜代码不存在'
            if int(text[2]) > 12 or int(text[2]) < 1:
                return '时间设置错误'
            if not zgcode in lzgs:
                datemax = datetime.datetime.strptime('%s-%s-25' % (time.strftime("%Y",time.localtime(time.time())), text[2]),
                                                     "%Y-%m-%d").date()  # 带有年格式
                datemin = datemax - datetime.timedelta(seconds=60 * 60 * 24 * 30)
                datemax = datemax.strftime('%Y-%m-25')
                datemin = datemin.strftime('%Y-%m-26')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    return '@img@%s' % (
                    Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName']))
                else:
                    return ret
            else:
                #26-10
                datemax = datetime.datetime.strptime('%s-%s-10' % (time.strftime("%Y",time.localtime(time.time())), int(time.strftime("%m",time.localtime(time.time()))) - 1),
                                                     "%Y-%m-%d").date()  # 带有年格式
                datemin = datemax - datetime.timedelta(seconds=60 * 60 * 24 * 30)
                datemax = datemax.strftime('%Y-%m-10')
                datemin = datemin.strftime('%Y-%m-26')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    retpath=Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName'])
                    itchat.send('@img@%s' % (retpath),kwargs['FromUserName'])
                #10-25
                datemax = datetime.datetime.strptime('%s-%s-10' % (time.strftime("%Y",time.localtime(time.time())), int(time.strftime("%m",time.localtime(time.time()))) - 1),
                                                     "%Y-%m-%d").date()  # 带有年格式
                datemin = datemax.strftime('%Y-%m-11')
                datemax = datemax.strftime('%Y-%m-25')
                # logging.debug(datemax)
                # logging.debug(datemin)
                title, ret = wumis.Bill_Balance_select(zgcode, datemin, datemax)
                if title != False:
                    retpath=Images.Get_image_bill_balance(title, datemin, datemax, ret, kwargs['FromUserName'])
                    itchat.send('@img@%s' % (retpath), kwargs['FromUserName'])
    except BaseException as e:
        print(e)
        logger.debug('Send_bill_balance_teble')
        logger.debug(e)



#导购功能
#设置专柜
# def Set_zgcode(text,**kwargs):
#     try:
#         text=text.split(' ')
#         if len(text)!=2 and len(text)!=3:
#             return '指令错误'
#         if len(text)==2:
#             if _Fcunction.Judge_zgcode(text[1]):
#                 zgcode = Get_Branch(kwargs['FromUserName'])
#                 if zgcode != '11':
#                     return '设置失败,当前专柜代码为%s,需修改请咨询楼层主管' % zgcode
#                 Boxfriends.Set_zgcode(kwargs['FromUserName'], text[1])
#                 Boxfriends.Set_family(kwargs['FromUserName'],wumis.Get_zg_family(text[1]))
#                 return '设置成功'
#             else:
#                 return '没有该专柜'
#         if Get_right(kwargs['FromUserName'])>1:
#             if len(text) == 3:
#                 if _Fcunction.Judge_zgcode(text[2]):
#                     zgcode = text[2]
#                     Boxfriends.Set_zgcode(text[1], zgcode, mode=1)
#                     Boxfriends.Set_family(text[1], wumis.Get_zg_family(text[1]),mode=1)
#                     return '设置成功'
#                 else:
#                     return '没有该专柜'
#         else:
#             return '指令错误'
#
#     except BaseException as e:
#         logger.debug('Set_zgcode')
#         logger.debug(e)




#获取自身ID  修改专柜需要
def Get_my_id(text,**kwargs):
    try:
        return '用户ID：%s'% Boxfriends.Get_User_Information(kwargs['FromUserName'], 'id')
    except BaseException as e:
        logger.debug('Get_my_id')
        logger.debug(e)





#下面是管理员功能
#提升权限 通过id
def Top_Up_right(text,**kwargs):
    #提升权限
    text=text.split(' ')
    if len(text)!=3:
        return '指令错误'
    if int(text[2])>4:
        return  '权限设置错误 1-4'
    return Boxfriends.Top_Up_right(text[1],text[2])

#更新专柜信息
def update_zg(text,**kwargs):
    try:
        wumis.Update_zgname()
        return '更新成功'
    except BaseException as e:
        logger.debug('update_zg')
        logger.debug(e)
        return '更新失败'

# #管理员发送消息,搜索功能
# def Send_msg(text,**kwargs):
#     text1 = text
#     try:
#         text = text.split(' ')
#         sendstr = re.findall(r'\(([\S\s]+)\)', text1)
#         if len(sendstr) >= 0:
#             sendstr = sendstr[0]
#         else:
#             return 'error:指令错误'
#         if len(text) >= 2:
#             if re.match('family=(\d)', text[1]):
#                 family = re.match('family=(\d)', text[1]).group(1)
#                 if family == '4':
#                     Boxfriends.Send_msg_all(sendstr + '\n  Sender:Admin')
#                 else:
#                     Boxfriends.Send_msg_select(sendstr + '\n  Sender:Admin', family=family)
#             else:
#                 if re.match('[\u4e00-\u9fa5]', text[1]):
#                     Boxfriends.Send_msg_select(sendstr + '\n  Sender:Admin', RemarkName=text[1])
#                 elif re.match('\d+', text[1]):
#                     Boxfriends.Send_msg_select(sendstr + '\n  Sender:Admin', id=int(text[1]))
#     except IndexError as e:
#         logger.debug('Send_msg 指令错误')
#         return ('注意空格')