from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
#读取配置文件
app.config.from_object('config')

#创建数据库对象
db = SQLAlchemy(app)

#创建登录对象
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

#导入模版为全局变量
from .momentjs import momentjs
app.jinja_env.globals['momentjs'] = momentjs


from app import views, models


#if not app.debug:
import logging
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
app.logger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.info('microblog startup')
#清除微信运行日志


