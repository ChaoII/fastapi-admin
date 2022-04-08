# -*- coding: utf-8 -*-
"""
@Time ： 2022/1/4 13:43
@Auth ： Jolg
@File ：test.py
@IDE ：PyCharm

"""
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


app = FastAPI()


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )


@app.get("/")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}
if __name__ == "__main__":
    uvicorn.run(app='test:app', port=8080)