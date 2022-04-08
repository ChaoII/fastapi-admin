# -*- coding: utf-8 -*-
"""
@Time ： 2022/1/10 9:13
@Auth ： Jolg
@File ：menu.py
@IDE ：PyCharm

"""
from apps.base.log import logger, conf
from apps.base.conf import templates
import hashlib
import time
from jose import jwt
from apps.models import Users, AccessRecords, Menu
from apps.base.db import Newsession
from fastapi import Header, HTTPException, Request, APIRouter, Body, Depends
import time, datetime
from starlette.responses import RedirectResponse
from apps.base.middleware import ToLogin, UnicornException

route = APIRouter()
Templ = templates.TemplateResponse
from apps.user.user import CurrentUser, CurrentUserRedir
from pydantic import BaseModel


def finemenu(parment):
    session = Newsession()
    # menu = session.query(Menu).filter(Menu.parent == parment).order_by(Menu.softd).all()
    menu = session.query(Menu).filter(Menu.parent == parment).all()
    routemenus = []
    for p in range(len(menu)):
        routemenu = {}
        routemenu['path'] = menu[p].path
        routemenu['name'] = menu[p].name
        routemenu['component'] = menu[p].component
        routemenu['meta'] = {}
        routemenu['meta']['title'] = menu[p].title
        routemenu['meta']['isLink'] = True if menu[p].link == '1' else False
        routemenu['meta']['isHide'] = True if menu[p].ishide == '1' else False
        routemenu['meta']['isAffix'] = True if menu[p].isaffix == '1' else False
        routemenu['meta']['isIframe'] = True if menu[p].isiframe == '1' else False
        routemenu['meta']['icon'] = menu[p].icon
        routemenu['meta']['softd'] = menu[p].softd
        logger.debug(menu[p].defpage)
        if menu[p].defpage != None:
            menu[p].children = finemenu(menu[p].id)
            routemenu['children'] = finemenu(menu[p].id)
        routemenus.append(routemenu)
    return routemenus


@logger.catch()
@route.get("/user/getMenu", summary='用户菜单')
def getMenu(user: CurrentUser = Depends(CurrentUser)):
    logger.debug(user)
    data = finemenu(None)
    logger.debug(data)
    da = {"msg": "ok!", "type": "adminMenu", "code": 0, "data": data}
    return da


@logger.catch()
@route.get("/user/getMenu2", summary='用户菜单')
def getMenu2(user: CurrentUser = Depends(CurrentUser)):
    logger.debug(user)
    data = {
        "code": 0,
        "type": "adminMenu",
        "data": [
            {
                "path": "/home",
                "name": "home",
                "component": "home/index",
                "meta": {
                    "title": "message.router.home",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": True,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-shouye"
                }
            },
            {
                "path": "/system",
                "name": "system",
                "component": "layout/routerView/parent",
                "redirect": "/system/menu",
                "meta": {
                    "title": "message.router.system",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin"],
                    "icon": "iconfont icon-xitongshezhi"
                },
                "children": [
                    {
                        "path": "/system/menu",
                        "name": "systemMenu",
                        "component": "system/menu/index",
                        "meta": {
                            "title": "message.router.systemMenu",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin"],
                            "icon": "iconfont icon-caidan"
                        }
                    },
                    {
                        "path": "/system/user",
                        "name": "systemUser",
                        "component": "system/user/index",
                        "meta": {
                            "title": "message.router.systemUser",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin"],
                            "icon": "iconfont icon-icon-"
                        }
                    }
                ]
            },
            {
                "path": "/limits",
                "name": "limits",
                "component": "layout/routerView/parent",
                "redirect": "/limits/frontEnd",
                "meta": {
                    "title": "message.router.limits",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-quanxian"
                },
                "children": [
                    {
                        "path": "/limits/backEnd",
                        "name": "limitsBackEnd",
                        "component": "layout/routerView/parent",
                        "meta": {
                            "title": "message.router.limitsBackEnd",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin", "common"]
                        },
                        "children": [
                            {
                                "path": "/limits/backEnd/page",
                                "name": "limitsBackEndEndPage",
                                "component": "limits/backEnd/page/index",
                                "meta": {
                                    "title": "message.router.limitsBackEndEndPage",
                                    "isLink": "",
                                    "isHide": False,
                                    "isKeepAlive": True,
                                    "isAffix": False,
                                    "isIframe": False,
                                    "roles": ["admin", "common"]
                                }
                            }
                        ]
                    }
                ]
            },
            {
                "path": "/menu",
                "name": "menu",
                "component": "layout/routerView/parent",
                "redirect": "/menu/menu1",
                "meta": {
                    "title": "message.router.menu",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-caidan"
                },
                "children": [
                    {
                        "path": "/menu/menu1",
                        "name": "menu1",
                        "component": "layout/routerView/parent",
                        "redirect": "/menu/menu1/menu11",
                        "meta": {
                            "title": "message.router.menu1",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin", "common"],
                            "icon": "iconfont icon-caidan"
                        },
                        "children": [
                            {
                                "path": "/menu/menu1/menu11",
                                "name": "menu11",
                                "component": "menu/menu1/menu11/index",
                                "meta": {
                                    "title": "message.router.menu11",
                                    "isLink": "",
                                    "isHide": False,
                                    "isKeepAlive": True,
                                    "isAffix": False,
                                    "isIframe": False,
                                    "roles": ["admin", "common"],
                                    "icon": "iconfont icon-caidan"
                                }
                            },
                            {
                                "path": "/menu/menu1/menu12",
                                "name": "menu12",
                                "component": "layout/routerView/parent",
                                "redirect": "/menu/menu1/menu12/menu121",
                                "meta": {
                                    "title": "message.router.menu12",
                                    "isLink": "",
                                    "isHide": False,
                                    "isKeepAlive": True,
                                    "isAffix": False,
                                    "isIframe": False,
                                    "roles": ["admin", "common"],
                                    "icon": "iconfont icon-caidan"
                                },
                                "children": [
                                    {
                                        "path": "/menu/menu1/menu12/menu121",
                                        "name": "menu121",
                                        "component": "menu/menu1/menu12/menu121/index",
                                        "meta": {
                                            "title": "message.router.menu121",
                                            "isLink": "",
                                            "isHide": False,
                                            "isKeepAlive": True,
                                            "isAffix": False,
                                            "isIframe": False,
                                            "roles": ["admin", "common"],
                                            "icon": "iconfont icon-caidan"
                                        }
                                    },
                                    {
                                        "path": "/menu/menu1/menu12/menu122",
                                        "name": "menu122",
                                        "component": "menu/menu1/menu12/menu122/index",
                                        "meta": {
                                            "title": "message.router.menu122",
                                            "isLink": "",
                                            "isHide": False,
                                            "isKeepAlive": True,
                                            "isAffix": False,
                                            "isIframe": False,
                                            "roles": ["admin", "common"],
                                            "icon": "iconfont icon-caidan"
                                        }
                                    }
                                ]
                            },
                            {
                                "path": "/menu/menu1/menu13",
                                "name": "menu13",
                                "component": "menu/menu1/menu13/index",
                                "meta": {
                                    "title": "message.router.menu13",
                                    "isLink": "",
                                    "isHide": False,
                                    "isKeepAlive": True,
                                    "isAffix": False,
                                    "isIframe": False,
                                    "roles": ["admin", "common"],
                                    "icon": "iconfont icon-caidan"
                                }
                            }
                        ]
                    },
                    {
                        "path": "/menu/menu2",
                        "name": "menu2",
                        "component": "menu/menu2/index",
                        "meta": {
                            "title": "message.router.menu2",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin", "common"],
                            "icon": "iconfont icon-caidan"
                        }
                    }
                ]
            },
            {
                "path": "/fun",
                "name": "funIndex",
                "component": "layout/routerView/parent",
                "redirect": "/fun/tagsView",
                "meta": {
                    "title": "message.router.funIndex",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-crew_feature"
                },
                "children": [
                    {
                        "path": "/fun/tagsView",
                        "name": "funTagsView",
                        "component": "fun/tagsView/index",
                        "meta": {
                            "title": "message.router.funTagsView",
                            "isLink": "",
                            "isHide": False,
                            "isKeepAlive": True,
                            "isAffix": False,
                            "isIframe": False,
                            "roles": ["admin", "common"],
                            "icon": "elementPointer"
                        }
                    }
                ]
            },
            {
                "path": "/chart",
                "name": "chartIndex",
                "component": "chart/index",
                "meta": {
                    "title": "message.router.chartIndex",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-ico_shuju"
                }
            },
            {
                "path": "/personal",
                "name": "personal",
                "component": "personal/index",
                "meta": {
                    "title": "message.router.personal",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-gerenzhongxin"
                }
            },
            {
                "path": "/tools",
                "name": "tools",
                "component": "tools/index",
                "meta": {
                    "title": "message.router.tools",
                    "isLink": "",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin", "common"],
                    "icon": "iconfont icon-gongju"
                }
            },
            {
                "path": "/link",
                "name": "layoutLinkView",
                "component": "layout/routerView/link",
                "meta": {
                    "title": "message.router.layoutLinkView",
                    "isLink": "https://element-plus.gitee.io/#/zh-CN/component/installation",
                    "isHide": False,
                    "isKeepAlive": False,
                    "isAffix": False,
                    "isIframe": False,
                    "roles": ["admin"],
                    "icon": "iconfont icon-caozuo-wailian"
                }
            },
            {
                "path": "/iframes",
                "name": "layoutIfameView",
                "component": "layout/routerView/iframe",
                "meta": {
                    "title": "message.router.layoutIfameView",
                    "isLink": "https://gitee.com/lyt-top/vue-next-admin",
                    "isHide": False,
                    "isKeepAlive": True,
                    "isAffix": True,
                    "isIframe": True,
                    "roles": ["admin"],
                    "icon": "iconfont icon-neiqianshujuchucun"
                }
            }
        ]
    }
    return data
