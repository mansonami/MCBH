import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
file_handler = RotatingFileHandler('tmp/bot.log', 'a', 1 * 1024 * 1024, 10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
logger.addHandler(file_handler)
logger.addHandler(ch)
logger.info('bot startup')
