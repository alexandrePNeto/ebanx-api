### Tools 🔨
 - Python 3.13 # https://www.python.org/ftp/python/3.13.6/python-3.13.6-amd64.exe
 - Framework: FastApi
 - Documentação automática: http://127.0.0.1:4800/docs#/
### How to run? 🏃‍♂️💨
 - Create environ:
    - > python -m venv venv
    - > pip install -r requirements.txt

 - Activate environ:
    - > .\venv\Scripts\activate

 - Start (--port == set api port):
    - > cd app
    - > fastapi dev main.py --port 4800
