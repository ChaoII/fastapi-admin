# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/29 16:18
@Auth ： Jolg
@File ：log.py
@IDE ：PyCharm

"""
from loguru import logger
from apps.base.conf import BASE_DIR,conf,LogLevel
import os,sys

log_path = os.path.join(BASE_DIR, 'logs')
log_file = os.path.join(log_path, f'BaseApi.log')
logger.remove()
logger.add(sys.stderr, level=LogLevel)
logger.add(log_file, level=LogLevel)

def initlog():
    if not os.path.exists(log_path):
        os.mkdir(log_path)

