# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 作者   : 王宗龙
# 文件     : user.py
# 时间     : 2020/12/9 15:30
# 开发工具 : PyCharm


from apps.base.log import logger, conf
from apps.base.conf import templates
import hashlib
import time
from jose import jwt
from apps.models import Users, AccessRecords
from apps.base.db import Newsession
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends
import time, datetime
from starlette.responses import RedirectResponse
from apps.base.middleware import ToLogin, UnicornException

route = APIRouter()
Templ = templates.TemplateResponse


def md5value(s):
    md5 = hashlib.md5()
    md5.update(s)
    return md5.hexdigest()


@logger.catch()
@route.post("/user/signIn", summary='用户登录，获取TOKEN')
def login(request: Request, username: str = Body(...), password: str = Body(...), ):
    '''TOKEN 获取接口
    ============================
    '''
    logger.debug(username)
    session = Newsession()
    user = session.query(Users).filter_by(name=username, passwd=md5value(password.encode())).first()
    logger.debug(user)
    if user:
        user.lastlogin = datetime.datetime.now()
        # logger.debug(user.lastlogin.strftime('%Y-%m-%d %H:%M:%S'))
        info = {"id": user.id, "username": user.name, "nicename": user.nicename,
                "roles": ['admin'], 'BtnList': ['btn.add', 'btn.del', 'btn.edit', 'btn.link'],
                "photo": 'static/photo/head.jpg', "loginip": request.client.host,
                "lastlogin": user.lastlogin.strftime('%Y-%m-%d %H:%M:%S')}
        payload = {
            "iat": int(time.time()),
            "exp": int(time.time()) + 86400 * 7,
            # token签发者
            'iss': 'zlWang',
            'data': info,
            "jti": "4f1g23a12aa"
        }
        # 生成token
        token = jwt.encode(payload, conf.SECRET_KEY, algorithm='HS512', )
        data = {"msg": "登录成功!", "token": token, "code": 1, "userinfo": info}
        session.add(user)
        # session.commit()
    else:
        data = {"msg": "登录失败!", "code": -1}
    return data


@logger.catch()
class User_info:
    def __init__(self, userid):
        self.USERID = userid


class CurrentUser:
    def __init__(self, request: Request, TOKEN: str = Header(None), QTOKEN: str = None):
        if TOKEN or QTOKEN:
            tk = TOKEN if TOKEN else QTOKEN
            users = ''
            try:
                users = jwt.decode(tk, conf.SECRET_KEY, algorithms=['HS512'])
            except Exception as e:
                logger.error(e)
            if users:
                user = users['data']
                logger.debug(user)
                self.userid = user['id']
                self.username = user['username']
                self.nicename = user['nicename']
                # logger.debug(conf.access_records)
                if conf.access_records:
                    accessrecords = AccessRecords(userid=user['id'], username=user['username'],
                                                  nicename=user['nicename'], url=str(request.url),
                                                  method=request.method)
                    # logger.debug(accessrecords.nicename)
                    session = Newsession()
                    session.add(accessrecords)
                    session.commit()
                return
        logger.debug("未登录")
        data = {"msg": "用户未登录!", "code": -1}
        raise HTTPException(status_code=200, detail=data)


@logger.catch()
@route.get("/user/getUser", summary='用户列表')
def getMenu(searstr: str = '', user: CurrentUser = Depends(CurrentUser)):
    session = Newsession()
    user = session.query(Users).filter(Users.name.like(f'%{searstr}%')).limit(10).offset(0).all()
    ct = session.query(Users).count()
    data = {"msg": "ok!", "code": 1, "user": user, "total": ct}
    return data


@logger.catch()
@route.post("/user/addUser", summary='新增用户', )
def addUser(username: str = Body(...), nicename: str = Body(...), role: str = Body(...), password: str = Body(...),
            status: str = Body(...), user: CurrentUser = Depends(CurrentUser)):
    session = Newsession()
    user = session.query(Users).filter_by(name=username).first()
    if not user:
        logger.info(status)
        adduser = Users(name=username, nicename=nicename, role=role, passwd=md5value(password.encode()),
                        status=1 if status else 0)
        session.add(adduser)
        session.commit();
        session.flush()
        data = {"msg": "ok!", "code": 1}
    else:
        data = {"msg": "用户已存在!", "code": 0}
    return data


@logger.catch()
@route.post("/user/editUser", summary='编辑用户', )
def addUser(id: str = Body(...), name: str = Body(...), nicename: str = Body(...), role: str = Body(...),
            status: str = Body(...), user: CurrentUser = Depends(CurrentUser)):
    session = Newsession()
    session.query(Users).filter_by(id=id).update({"name": name, "nicename": nicename, "role": role, "status": status})
    session.commit()
    session.flush()
    data = {"msg": "ok!", "code": 1}
    return data


@logger.catch()
@route.post("/user/delUser", summary='删除用户', )
def delUser(userid: str = Body(...)):
    session = Newsession()
    user = session.query(Users).filter_by(id=userid).first()
    if user:
        session.delete(user)
        session.commit()
        session.flush()
        data = {"msg": "ok!", "code": 1}
    else:
        data = {"msg": "用户不存在!", "code": 0}
    return data


@logger.catch()
@route.get("/login", summary='用户登录web')
def login(request: Request):
    context = {'request': request, }
    return Templ('login.html', context)


class CurrentUserRedir:
    def __init__(self, request: Request, TOKEN: str = Header(None), QTOKEN: str = None):
        if TOKEN or QTOKEN:
            tk = TOKEN if TOKEN else QTOKEN
            users = ''
            try:
                users = jwt.decode(tk, conf.SECRET_KEY, algorithms=['HS512'])
            except Exception as e:
                logger.error(e)
            if users:
                user = users['data']
                logger.debug(user)
                self.userid = user['id']
                self.username = user['username']
                self.nicename = user['nicename']
                # logger.debug(conf.access_records)
                if conf.access_records:
                    accessrecords = AccessRecords(userid=user['id'], username=user['username'],
                                                  nicename=user['nicename'], url=str(request.url),
                                                  method=request.method)
                    # logger.debug(accessrecords.nicename)
                    session = Newsession()
                    session.add(accessrecords)
                    # session.commit()
                return
        else:
            raise ToLogin(url='/login')
