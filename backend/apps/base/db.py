# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/30 11:46
@Auth ： Jolg
@File ：db.py
@IDE ：PyCharm

"""
import pymysql

pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine
import os
from apps.base.conf import BASE_DIR, conf, mysqlconf, pgdbconf
from sqlalchemy.orm import sessionmaker

if conf.db == 'mysql':
    engine = create_engine(
        f"mysql://{mysqlconf.username}:{mysqlconf.password}@{mysqlconf.host}:{mysqlconf.port}/{mysqlconf.dbname}?charset=utf8",
        echo=conf.debug, pool_recycle=60 * 5)
elif conf.db == 'postgresql':
    engine = create_engine(
        f'postgresql+psycopg2://{pgdbconf.username}:{pgdbconf.password}@{pgdbconf.host}:{pgdbconf.port}/{pgdbconf.dbname}')
else:
    dbfile = os.path.join(BASE_DIR, 'DB.sqlite')
    engine = create_engine(f'sqlite:///{dbfile}', echo=conf.debug, pool_recycle=60 * 5,
                           connect_args={"check_same_thread": False})


# DbSession = sessionmaker(bind=engine,autocommit=True)
# # DbSession = sessionmaker(bind=engine)
# session = DbSession()

def Newsession():
    DbSession = sessionmaker(bind=engine)
    Session = DbSession()
    return Session
