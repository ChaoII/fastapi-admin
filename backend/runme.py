# -*- coding: utf-8 -*-
"""
@Time ： 2021/12/29 16:12
@Auth ： Jolg
@File ：runme.py
@IDE ：PyCharm

"""
import uvicorn
from apps.base.hello import hello, logger
from apps.base.conf import conf, LogLevel
from apps.route import createapp

app = createapp()
if __name__ == "__main__":
    try:
        hello()
        uvicorn.run(app='runme:app',
                    host=conf.host,
                    port=conf.port,
                    reload=True,
                    debug=conf.debug,
                    log_level=LogLevel.lower(),
                    log_config="apps/base/UlogConf.json"
                    )
    except:
        logger.exception("服务异常！")
