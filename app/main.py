# !/usr/bin/python
# vi: fileencoding=utf-8
from fastapi import FastAPI

from dotenv import load_dotenv

from web.routes import init_app

app: FastAPI = FastAPI()

if not load_dotenv("../.env"):
    load_dotenv(".env")

init_app(app)
