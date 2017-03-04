import json
import time
import shutil
import os
import psutil
from flask import g
from app import app
from config import WX_LOGIN_START_BAT,WX_QR_CODE_JPG,basedir,FUNCTIONAL_STATUS
from .models import Wxuser,Wxsetting
import socket
import win32api


def wx_login_bat(temp):
    '''

    :param temp: 时间戳参数
    :return: 图片名称
    '''
    if os.path.exists(WX_QR_CODE_JPG):
        os.remove(WX_QR_CODE_JPG)
    app.logger.debug(WX_LOGIN_START_BAT)
    win32api.ShellExecute(0, 'open', 'python.exe', 'mian.py', '', 1)
    img_path=os.path.join(basedir,'app','static','cache','%s.jpg'%temp)
    app.logger.debug(WX_QR_CODE_JPG)
    app.logger.debug(img_path)
    while 1:
        if os.path.exists(WX_QR_CODE_JPG):
            #移动图片到模版文件夹
            shutil.move(WX_QR_CODE_JPG,img_path)
            pid=getpid()
            g.user.set_wxpid(pid)
            return True
        time.sleep(1)

def wx_is_login_state():
    '''
    通过pid检测微信子进程是否还在运行
    :return:
    '''
    pid=g.user.get_wxpid()
    if psutil.pid_exists(pid):
        return True
    g.user.set_wxpid(999999)
    return False

def wx_logout():
    '''
    强行关闭微信pid
    :return:
    '''
    try:
        pid = g.user.get_wxpid()
        if psutil.pid_exists(pid):
            os.system('taskkill /PID %s /F /T' % pid)
            g.user.set_wxpid(999999)
        return '关闭微信成功'
    except:
        return '关闭微信成功'

def sendmsg(id,text):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = '%s (%s)'%(id,text)
    app.logger.debug(data)
    s.sendto(data.encode(), ('127.0.0.1', 9999))
    s.close()



def WX_user_setting(id,name,right):
    try:
        user=Wxuser.query.filter_by(id=id).first()
        user.right=right
        if user.remarkname!=name:
            user.remarkname = name
            setrickname(id,name)
        user.save()
        return '修改成功'
    except:
        return '修改失败'


def setrickname(id,name):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = 'name %s %s'%(id,name)
    app.logger.debug(data)
    s.sendto(data.encode(), ('127.0.0.1', 9999))
    s.close()


def getpid():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto('pid'.encode(), ('127.0.0.1', 9999))
    ret=s.recv(1024).decode('utf-8')
    s.close()
    return ret

def Update_setting():
    q=Wxsetting().getsetting()
    with open(FUNCTIONAL_STATUS,'w') as f:
        f.write(json.dumps(q))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = 'Update'
    app.logger.debug(data)
    s.sendto(data.encode(), ('127.0.0.1', 9999))
    s.close()
