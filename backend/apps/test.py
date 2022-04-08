# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/30 9:25
@Auth ： Jolg
@File ：test.py
@IDE ：PyCharm

"""
from apps.base.log import logger
from apps.user.user import CurrentUser,CurrentUserRedir
from fastapi import APIRouter, Depends

route = APIRouter()


@logger.catch()
@route.get("/",summary='测试')
def login(user : CurrentUser= Depends(CurrentUserRedir)):
    '''TOKEN 获取接口
    ============================
    '''
    logger.debug(user.username)
    data = {"msg": "oooooooooooo!", "code": 1,"user":user}
    return data