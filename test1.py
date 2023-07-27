import asyncio
import base64
from cryptography import fernet
from cryptography.fernet import Fernet
from aiohttp import web, ClientSession
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session import *
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from werkzeug.wsgi import DispatcherMiddleware

# Basic Import Files
from pymongo import MongoClient
import bcrypt
import random
import json
import aiohttp
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os
from aiohttp_wsgi import WSGIHandler

# Directory Import Files
# from chatlib import *
from common.commonFunctions import *

from Database.databaseConfig import *
from Database.databaseConfig import GroupList, Users, UserDetails, EmailVerification, Messages, websockets, test, workSpace
from SocketOnResponse.responseSocket import respondToSocket




routes = web.RouteTableDef()
# websockets = set()
# history = []
# test = {}


@routes.get('/')
async def workspace_(request):
    mail_context = {}
    response = aiohttp_jinja2.render_template("workspace.html", request, context=mail_context)
    return response



@routes.get('/createWorkSpace')
async def _createWorkSpace(request):
    context = {}
    response = aiohttp_jinja2.render_template("createWorkSpace.html", request,context=context)
    
    return response


# async def handler(request):  # main application's handler
#     subapp = request.app['subapp']
#     url = subapp.router['name'].url_for()

async def handler(request):
    return web.Response()

# subapp = web.Application()
# subapp.router.add_get('/', handler)
# subapp.router.add_get('/login', handler, name='hello')




# subapp.router.add_get('/', handler)

subapp = web.Application()
subapp.router.add_get('/', workspace_)
subapp.router.add_get('/createWorkSpace', _createWorkSpace)

# subapp.add_subapp('/sub/', subsubapp)

app = web.Application()
app.add_subapp('/messenger/', subapp)


# Adding Template files to the Project
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))

# Adding Static files and folder to the Project.
# Ref:- https://github.com/aio-libs/aiohttp/blob/57df1d71a5322a599110bb4011ed7e28b28e6114/docs/web_advanced.rst
staticdir_ = os.path.join(os.getcwd(), "static")
cssdir_ = os.path.join(os.getcwd(), "static\css")
jsdir_ = os.path.join(os.getcwd(), "static\js")
filesdir_ = os.path.join(os.getcwd(), "static\\files")

app.add_routes([web.static('/static/', staticdir_)])
app.add_routes([web.static('/static/css/', cssdir_)])
app.add_routes([web.static('/static/js/', jsdir_)])
app.add_routes([web.static('/static/files/', filesdir_)])


if __name__ == '__main__':
    web.run_app(app)
# web.run_app(app, host='127.0.0.1', port=8080)