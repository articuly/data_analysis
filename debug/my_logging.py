# coding:utf-8

import logging

filename = 'mylog.txt'
filemode = 'a'
format = '[%(name)s %(levelname)s] %(process)d file:%(pathname)s on %(lineno)d, %(message)s at %(asctime)s'

logging.basicConfig(filename=filename, filemode=filemode, format=format, level=20)


def create_logger(name=None):
    return logging.getLogger(name)
