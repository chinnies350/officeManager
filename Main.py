import aiohttp
from aiohttp import web
import aiohttp_jinja2
from chat import app




if __name__ == '__main__':
    # ip = "0.0.0.0"
    ip="127.0.0.1"
    web.run_app(app,host=ip, port=10000)
    # web.run_app(app)