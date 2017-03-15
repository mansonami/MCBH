
import pyodbc
import time
import json
import datetime
import bot.models._Fcunction
from bot import logger
from config import ZG_NAME_JSON_PATH


WUMIS="DSN=wumis;UID=sa;pwd=wuitghxx"
#===========

#============

with open(ZG_NAME_JSON_PATH,'r') as f:
    ZG_NAME = json.loads(f.read())

#销售对账单查询
def Get_sell(datemin=time.strftime("%m-%d-%Y",time.localtime(time.time())),datemax=time.strftime("%m-%d-%Y",time.localtime(time.time())),zgcode='%',depart='%',mode=0):
    global WUMIS
    '''
    :param datemin: 查询开始时间
    :param datemax: 查询结束时间
    :param zgcode: 专柜代码
    :param depart: 楼称
    :param mode: 查询模式  0为今日销售,1为销售报表，####2为单柜销售总计
    :return:
    '''
    if depart!='%':
        depart='0%s'%depart
    try:
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        cursor.execute(
            '''
            exec dbo.up_report_zgsell
            @startdate = '%s 0:0:0',
            @enddate = '%s 23:59:59',
            @as_organ = NULL ,
            @as_depart = '%s',
            @as_receid = '%%',
            @as_op_depart = '8023',
            @as_zgcode = '%s',
            @as_taxtype = '%%',
            @ai_cxfs = 9
            '''%(datemin,datemax,depart,zgcode)
        )
        if mode==0:#今日销售模式
            sale_1=0
            sale_2=0
            sale_3=0
            sale_bbx=0
            sale_all=0
            for row in cursor:
                #print(row)
                if row[0]=='01':
                    sale_1=sale_1+row[8]
                elif row[0]=='02':
                    if row[1]=='510003':
                        sale_bbx=sale_bbx+row[8]
                    else:
                        sale_2 = sale_2 + row[8]
                elif row[0]=='03':
                    sale_3 = sale_3 + row[8]
            sale_all=sale_1+sale_2+sale_3
            #print('今日销售:\n1F:%.2f\n2F:%.2f\n3F:%.2f\n总计:%.2f\n波波熊:%.2f'% (sale_1, sale_2, sale_3, sale_all,sale_bbx))
            if datemin==datemax and datemin==time.strftime("%m-%d-%Y"):
                return '今日销售:\n1F:%.2f\n2F:%.2f\n3F:%.2f\n总计:%.2f\n波波熊:%.2f'% (sale_1, sale_2, sale_3, sale_all,sale_bbx)
            elif datemin==datemax:
                return '%s 销售:\n1F:%.2f\n2F:%.2f\n3F:%.2f\n总计:%.2f\n波波熊:%.2f' % (datemin,sale_1, sale_2, sale_3, sale_all, sale_bbx)
            else:
                return '%s---%s 销售:\n1F:%.2f\n2F:%.2f\n3F:%.2f\n总计:%.2f\n波波熊:%.2f' % (datemin,datemax, sale_1, sale_2, sale_3, sale_all, sale_bbx)
        elif mode==1:#销售报表模式
            #print(depart)
            table_1f_str=''
            table_2f_str = ''
            table_3f_str = ''
            for row in cursor:
                if row[0]=='01':
                    table_1f_str = table_1f_str + '%s:%.2f/%.0f  ' % (ZG_NAME[row[1]], row[8], row[4])
                elif row[0]=='02':
                    table_2f_str = table_2f_str + '%s:%.2f/%.0f  ' % (ZG_NAME[row[1]], row[8], row[4])
                elif row[0]=='03':
                    table_3f_str = table_3f_str + '%s:%.2f/%.0f  ' % (ZG_NAME[row[1]], row[8], row[4])

            if depart=='%':
                return '%s\n%s\n%s'%(table_1f_str,table_2f_str,table_3f_str)
            elif depart=='01':
                return table_1f_str
            elif depart == '02':
                return table_2f_str
            elif depart == '03':
                return table_3f_str
    except BaseException as e :
        logger.info(e)
        return '联系管理员 更新专柜信息'
    finally:
        cursor.close()
        conn.close()
#查询专柜销售
def Get_zg_sell(zgcode,datemin=time.strftime("%m-%d-%Y",time.localtime(time.time())),datemax=time.strftime("%m-%d-%Y",time.localtime(time.time())),mode=0):
    '''

    :param zgcode: 专柜代码
    :param datemin: 开始日期
    :param datemax: 结束日期
    :param mode: 查询模式 0为详细，1为总计
    :return:
    '''
    ret = bot.models._Fcunction.Com_Date_Poor(datemin, datemax)
    global WUMIS
    #datemax = datetime.datetime.strptime(datemax, '%m-%d-%Y').date()
    try:
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        count=cursor.execute("select count(*) from provider WHERE code='%s'"%zgcode).fetchone()[0]
        if count==0: #专柜代码错误
            return False
        if mode==0:
            datemin = datetime.datetime.strptime(datemin, '%m-%d-%Y').date()  # 字串符 转为时间
            ret_str = '       %s   \n' % ZG_NAME[zgcode]

            for n in range(ret + 1):
                ret_date = datemin + datetime.timedelta(days=n)
                ret_date = ret_date.strftime('%m-%d-%Y')
                row = cursor.execute(
                    '''
                                exec dbo.up_report_zgsell
                                @startdate = '%s 0:0:0',
                                @enddate = '%s 23:59:59',
                                @as_organ = NULL ,
                                @as_depart = '%%',
                                @as_receid = '%%',
                                @as_op_depart = '8023',
                                @as_zgcode = '%s',
                                @as_taxtype = '%%',
                                @ai_cxfs = 9
                            ''' % (ret_date, ret_date, zgcode)
                ).fetchone()[8]
                ret_str = ret_str + '%s:%.2f\n' % (ret_date, row)
            return ret_str
        elif mode==1:
            count = cursor.execute(
                '''
                            exec dbo.up_report_zgsell
                            @startdate = '%s 0:0:0',
                            @enddate = '%s 23:59:59',
                            @as_organ = NULL ,
                            @as_depart = '%%',
                            @as_receid = '%%',
                            @as_op_depart = '8023',
                            @as_zgcode = '%s',
                            @as_taxtype = '%%',
                            @ai_cxfs = 9
                        ''' % (datemin, datemax, zgcode)
            ).fetchone()[8]
            if datemin == datemax and datemin == time.strftime("%m-%d-%Y"):
                return '    %s\n今日销售:%.2f' % (ZG_NAME[zgcode], count)
            elif datemin == datemax:
                return '       %s\n%s:%.2f' % (ZG_NAME[zgcode],datemin,count)
            else:
                return '         %s\n%s——%s:\n       %.2f'%(ZG_NAME[zgcode],datemin,datemax,count)
    finally:
        cursor.close()
        conn.close()
#查询对账单
def Bill_Balance_select(zgcode,datamin,datemax):
    try:
        global WUMIS
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        count = cursor.execute('''
SELECT BALANCE_FATH.ID,
PROVIDER.NAME
FROM BALANCE_FATH,
PROVIDER
WHERE (balance_fath.provider LIKE "%s"
       AND balance_fath.enddate >= "%s"
       AND balance_fath.enddate <= "%s")
  AND verifier IS NOT NULL
  AND verifier <> ""
  AND TYPE = 3 AND ( PROVIDER.Code like "%s")'''%(zgcode,datamin,datemax,zgcode)).fetchone()
        title=False
        if count==None:
            count='对账单还未生成'
            return False,count
        else:
            title = '[%s] %s' % (zgcode, bot.models._Fcunction.Decode_text(count[1]))
            count=count[0] #单据号
        #查询扣费详细
            logger.debug(title)
        count = cursor.execute('''exec dbo.up_bill_balance_prn_ly_mx @as_billid = '%s' '''%count).fetchall()
        logger.debug(count)
        return title,count
    except BaseException as e:
        logger.info(e)
    finally:
        cursor.close()
        conn.close()
        return title, count


def Get_zg_family(zgcode):
    global WUMIS
    try:
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        count = cursor.execute('''  SELECT SELL_DATA.depart FROM COMMODITY,SELL_DATA WHERE ( commodity.provider like "%s")  and  ( COMMODITY.CODE = SELL_DATA.CODE )'''%zgcode).fetchone()[0]
        if count=='01':
            return '1'
        elif count=='02':
            return '2'
        elif count=='03':
            return '3'
    except BaseException as e:
        logger.debug(e)
        return ''
    finally:
        cursor.close()
        conn.close()




#更新专柜信息
def Update_zgname():
    global WUMIS,ZG_NAME
    try:
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        count=cursor.execute('''
        Select PROVIDER.code,PROVIDER.name from PROVIDER
        ''').fetchall()
        for row in count:
            ZG_NAME[row[0]]=bot.models._Fcunction.Decode_text(row[1])
            with open(ZG_NAME_JSON_PATH,'w') as f:
                f.write(json.dumps(ZG_NAME))
            bot.models._Fcunction.Update_zgcode()
    except BaseException as e:
        logger.debug(e)
    finally:
        cursor.close()
        conn.close()

def Vip_query_Counters(zgcode):
    global WUMIS,ZG_NAME
    try:
        conn = pyodbc.connect(WUMIS,autocommit=True)
        cursor = conn.cursor()
        count = cursor.execute(''' select COMMODITY.NAME from vip_sell,commodity WHERE (vip_sell.vipid="%s") and (vip_sell.code=commodity.code)
'''%zgcode).fetchall()
        ret=[]
        for row in count:
            ret.append(bot.models._Fcunction.Decode_text(row[0]))
        ret=list(set(ret))
        if len(ret)==0:
            return False
        return ret
    except BaseException as e:
        return '查询无结果 %s'%e
    finally:
        cursor.close()
        conn.close()



if __name__=='__main__':
    pass
