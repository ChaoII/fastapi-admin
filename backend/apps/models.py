# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/30 13:21
@Auth ： Jolg
@File ：models.py
@IDE ：PyCharm

"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from apps.base.db import engine, Newsession
import time, datetime
from sqlalchemy.sql import func
from apps.base.log import logger

Base = declarative_base()


class Basejson():
    def json(self):
        dict = self.__dict__
        if "_sa_instance_state" in dict:
            del dict["_sa_instance_state"]
        return dict


class Users(Base, Basejson):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    passwd = Column(String(64))
    nicename = Column(String(64))
    role = Column(String(64))
    status = Column(String(64), default=1)
    create = Column(DateTime(), default=datetime.datetime.now())
    lastlogin = Column(DateTime())

    def __init__(self, name, nicename, passwd, role, status):
        self.name = name
        self.nicename = nicename
        self.passwd = passwd
        self.role = role
        self.status = status
    # def __str__(self):
    #     return self.name


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True)
    parent = Column(Integer)
    path = Column(String(64))
    name = Column(String(64))
    component = Column(String(64))
    icon = Column(String(64))
    link = Column(String(640))
    ishide = Column(String(64), default=1)
    isaffix = Column(String(64), default=1)
    isiframe = Column(String(64), default=1)
    defpage = Column(String(64))
    title = Column(String(64))
    softd = Column(Integer)
    create = Column(DateTime(), default=datetime.datetime.now())
    lastupdata = Column(DateTime())


class AccessRecords(Base):
    __tablename__ = "accessrecords"
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    username = Column(String(64))
    nicename = Column(String(164))
    url = Column(String(640))
    method = Column(String(64))
    access_date = Column(DateTime(), default=datetime.datetime.now())
    # access_date =Column(DateTime,default=time.time())


def inituser():
    session = Newsession()
    user = session.query(Users).filter_by(name='admin').first()
    if not user:
        adminuser = Users(name='admin', nicename="管理员", role='admin', passwd='21232f297a57a5a743894a0e4a801fc3',
                          status='1')
        session.add(adminuser)
        session.commit();
        session.flush()


def initmenu():
    defaultmenu = [
        [1, None, '/home', 'home', 'home/index', 'iconfont icon-shouye', None, 0, 1, 0, None, 'message.router.home', 1],
        [2, None, '/system', 'system', 'layout/routerView/parent', 'iconfont icon-xitongshezhi', None, 0, 0, 0,
         '/system/menu', 'message.router.system', 2],
        [3, 2, '/system/menu', 'systemMenu', 'system/menu/index', 'iconfont icon-caidan', None, 0, 0, 0, None,
         'message.router.systemMenu', 1],
        [4, 2, '/system/user', 'systemUser', 'system/user/index', 'iconfont icon-icon-', None, 0, 0, 0, None,
         'message.router.systemUser', 2],
    ]
    session = Newsession()
    for p in defaultmenu:
        menu = session.query(Menu).filter_by(id=p[0]).first()
        if not menu:
            menumod = Menu(id=p[0], parent=p[1], path=p[2], name=p[3], component=p[4], icon=p[5],
                           link=p[6], ishide=p[7], isaffix=p[8], isiframe=p[9], defpage=p[10], title=p[11], softd=p[12])
            session.add(menumod)
            session.commit()
            session.flush()


def initdb():
    Base.metadata.create_all(engine)
    inituser()
    initmenu()
