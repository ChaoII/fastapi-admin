# !/usr/bin/env Python3
# -*- coding: utf-8 -*-
# 作者   : 王宗龙
# 文件     : route
# 时间     : 2020/12/9 11:45
# 开发工具 : PyCharm


from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

# 导入项目view
# from apps import user,test
from apps.user import user, menu
from apps import test
from apps.base.middleware import register_cors, register_exception
from apps.base.conf import conf


def createapp():
    app = FastAPI(
        title=conf.title,
        description=conf.description,
        version=conf.VERSION,
    )
    app.mount('/static', StaticFiles(directory='apps/static'), name='static')

    # 用户相关
    app.include_router(user.route, tags=["用户"])
    app.include_router(menu.route, tags=["菜单"])
    app.include_router(test.route, tags=["测试"])

    # @app.get("/")
    # def home():
    #     return RedirectResponse(url="/otdisk/index.html")

    register_cors(app)  # 跨域设置
    # register_exception(app)

    return app
