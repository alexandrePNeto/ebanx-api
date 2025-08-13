# !/usr/bin/python
# vi: fileencoding=utf-8
from http import HTTPMethod

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse

from controllers.account import Account

PATH            = 0
HANDLER         = 2
CONTROLLER      = 1
HTTP_METHOD     = 3
RESPONSE_TYPE   = 4

routes: list = (
    # 0 - PATH           # 1 - CONTROLLER            # 2 - HANDLER              # 3 - HTTP MTHOD             # 4 - RESPONSE TYPE
    ("/reset",           Account,                    "reset",                   HTTPMethod.POST,             PlainTextResponse),
    ("/event",           Account,                    "event",                   HTTPMethod.POST,             JSONResponse),
    ("/balance",         Account,                    "balance",                 HTTPMethod.GET,              JSONResponse),
)

def init_app(app: FastAPI) -> None:
    for route in routes:
        app.add_api_route(
            path=route[PATH],
            methods=[route[HTTP_METHOD]],
            endpoint=eval("__import__('%s', None, locals(), ['%s']).%s().%s"
                % (route[CONTROLLER].__module__, route[CONTROLLER].__name__, route[CONTROLLER].__name__, route[HANDLER])),
            response_class=route[RESPONSE_TYPE]
        )
