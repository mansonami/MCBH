import os

#数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'mysql://root:a845331767@localhost:3306/test'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5


#表单验证配置
CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

POSTS_PER_PAGE=3


#微信启动脚本路径
WX_LOGIN_START_BAT=os.path.join(basedir, 'bot','start.bat')
WX_QR_CODE_JPG=os.path.join(basedir,'QR.jpg')#微信验证码图片
if os.path.exists(WX_QR_CODE_JPG):
    os.remove(WX_QR_CODE_JPG)



#机器人配置
ZG_NAME_JSON_PATH=os.path.join(basedir,'ZG_NAME.json')
BALANCE_BABLE_IMG_PATH=os.path.join(basedir,'bot','bill.png')
TEMPORARY_PATH=os.path.join(basedir,'bot','temporary')

BOT_SQLALCHEMY_DATABASE_URI =os.path.join(basedir, 'bot.db')

