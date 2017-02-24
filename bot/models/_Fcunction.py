import datetime
import json
from bot import logger

from config import ZG_NAME_JSON_PATH

with open(ZG_NAME_JSON_PATH,'r') as f:
    ZG_NAME = json.loads(f.read())

def Com_Date_Poor(datemin,datemax,date_type='days'):
    '''
    计算时间差,用于循环
    :param datemin: 开始时间  %m-%d-%Y
    :param datemax: 结束时间
    :param date_type: 类型
    :return: 返回数字差
    '''
    datemin=datetime.datetime.strptime(datemin,'%m-%d-%Y').date()
    datemax = datetime.datetime.strptime(datemax, '%m-%d-%Y').date()
    if date_type=='days':
        ret = (datemax - datemin).days
        logger.debug(ret)
        return ret

def Decode_text(text):
    text=text.encode('cp850')
    return text.decode('gbk')

def Judge_zgcode(zgcode):
    if zgcode in ZG_NAME:
        return True
    else:
        return False

def Update_zgcode():
    global ZG_NAME
    with open(ZG_NAME_JSON_PATH, 'r') as f:
        ZG_NAME = json.loads(f.read())
