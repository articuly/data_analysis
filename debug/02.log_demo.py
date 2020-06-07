# coding:utf-8
from my_logging import create_logger

logger = create_logger('app')

logger.critical('这是关键的错误')
logger.error('这是错误')
logger.warning('这是警告')
logger.info('这是通知信息')
logger.debug('这是调试信息')
logger.log(30, 'warning...')
