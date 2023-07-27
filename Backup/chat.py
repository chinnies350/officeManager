# Primary Import Files
import asyncio
import datetime

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
# from flask import jsonify

# Directory Import Files
from chatlib import *
from databaseLib import *


routes = web.RouteTableDef()
websockets = set()
history = []
test = {}


# For Database connections Refer The Import File "databaseLib.py"
# For the Other Basic Related Functions Refer The Import File "chatlib.py"
client = MongoClient('mongodb://192.168.1.169:27017/')
db = client.MadhukaranDb
message = db['Messages']


# Login/Home page Get Form
@routes.get('/', name='hello')
async def hello(request):

    # hello = "Testing"
    context = {
        # 'Test': hello,
    }

    response = aiohttp_jinja2.render_template("login.html", request,
                                              context=context)

    # ----------------------------IGNORE -------------------------#
    # This Box is included for the Refrence Purpose.              #
    # This is generated when "Aio implemented with Jinja2"        #
    # Dated - 14/10-20 - BEAST                                    #
    #                                                             #
    # with open('templates/login.html', 'rb') as f:               #
    #     return web.Response(                                    #
    #         body=f.read().decode('utf8'),                       #
    #         content_type='text/html')                           #
    # ----------------------------IGNORE -------------------------#
    return response


# SignUp Get Form
@routes.get('/signup', name='signup')
async def signup_(request):
    # hello = "Testing"
    context = {
        # 'Test1': hello,
    }

    response = aiohttp_jinja2.render_template("signup.html", request,
                                              context=context)

    # ----------------------------IGNORE -------------------------#
    # This Box is included for the Refrence Purpose.              #
    # This is generated when "Aio implemented with Jinja2"        #
    # Dated - 14/10-20 - BEAST                                    #
    #                                                             #
    # with open('templates/signup.html', 'rb') as f:              #
    #     return web.Response(                                    #
    #         body=f.read().decode('utf8'),                       #
    #         content_type='text/html')                           #
    # ----------------------------IGNORE -------------------------#

    return response


# SignUp Post Form
@routes.post('/signup', name='signup')
async def signup(request):
    user_data = await request.post()

    u_name = user_data.get('username')
    u_passw = user_data.get('password')

    hashedpw = bcrypt.hashpw(u_passw.encode('utf-8'), bcrypt.gensalt())
    if checkUserExist(u_name):
        context = {
            "errno": "Username Already Exist's. Try diffrent Username"
        }
        response = aiohttp_jinja2.render_template("signup.html", request,
                                                  context=context)
        return response
    else:
        context = {}
        user.insert({'username': u_name, 'password': hashedpw})
        response = aiohttp_jinja2.render_template(
            "signup.html", request, context=context)
        location = request.app.router['hello'].url_for()
        raise web.HTTPFound(location=location)
        return response


# Login Post Form
@routes.post('/')
async def login(request):
    form_data = await request.post()

    name = form_data.get('username')
    passw = form_data.get('password')

    if checkUserExist(name):
        if checkUserPass(name, passw):
            return web.HTTPFound(request.app.router['chat'].url_for(name=name))
        else:
            loginContext = {
                "errno": "Username or Password Does'nt Match either!"
            }
            response = aiohttp_jinja2.render_template("login.html", request,
                                                      context=loginContext)
            return response


@routes.get('/{name}/', name='chat')
async def chat_page(request):
    userList = getUserList()
    groups = getGroupList()

    context = {
        'Users': userList,
        'Groups': groups
    }
    response = aiohttp_jinja2.render_template("mainchat.html", request,
                                              context=context)

    # ----------------------------IGNORE -------------------------#
    # This Box is included for the Refrence Purpose.              #
    # This is generated when "Aio implemented with Jinja2"        #
    # Dated - 14/10-20 - BEAST                                    #
    #                                                             #
    # with open('templates/chat.html', 'rb') as f:                #
    #     return web.Response(                                    #
    #         body=f.read().decode('utf8'),                       #
    #         content_type='text/html')                           #
    # ----------------------------IGNORE -------------------------#
    return response


@routes.get('/{name}/ws/')
async def websocket(request):
    global name
    name = request.match_info['name']
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    print(name + "online!")
    for text in list(history):
        await ws.send_json(text)
    websockets.add(ws)
    test[name] = ws

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                # await send_to_all(name, msg.data)
                global toUser, Message, _from
                toUser, Message, _from = decrypt(msg.data)

                # storing Message to Database
                # _var = message.find_one(
                #     {"users": {"$eq": _from}}, {"_id": 0})
                # var_ = message.find_one(
                #     {"users": {"$eq": toUser}}, {"_id": 0})

                message.update({"User":_from}, {"$push":{toUser:{_from:Message}}})
                message.update({"User":toUser}, {"$push":{_from:{_from:Message}}})

                

                # if _var == None:
                #     if var_ == None:
                #         message.insert({"users": _from+toUser, "messages": []})
                #         message.update({'users': _from+toUser},
                #                        {'$push': {'messages': {_from: Message}}})
                #     else:
                #         message.update({'users': toUser+_from},
                #                        {'$push': {'messages': {_from: Message}}})
                # else:
                #     message.update({'users': _from+toUser},
                #                    {'$push': {'messages': {_from: Message}}})

                # Checks the User Based on the Messages Included Try Except Block if the User Sends the Message to
                # the Invalid User Websockets getting Closed. TRY EXCEPT prevents from the Websockets close.
                # the Message might append on the Frontend but will be Received on the Other User.
                if toUser == None or Message == None:
                    pass
                try:
                    await send_to_user(test[toUser], Message)

                except KeyError:
                    try:
                        x = groupList.find({"groupName": toUser}, {
                                           "_id": 0, "groupName": 0})
                        for data in x:
                            toto = data['Users']
                            await send_to_all(_from, toUser, Message, toto)
                    except KeyError:
                        print("Invalid ID! But The Message will be Appended")

            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    finally:
        websockets.remove(ws)

    print(name + "left")

    return ws


async def send_to_all(_from, toUser, message, toto):
    data = {"Type": "Group", "from": _from, "to": toUser, "Message": message}

    history.append(data)
    if len(history) > 20:
        del history[:10]

    tasks = set()
    web_ = websockets

    for ws in web_:
        if ws == test[_from]:
            pass
        else:
            tasks.add(asyncio.create_task(ws.send_json(data)))
            while tasks:
                done, tasks = await asyncio.wait(tasks)


# Sending Private message to the User
async def send_to_user(user, message):
    data = {"Type": "Private", "from": _from, "to": toUser, "Message": message}
    # await user.send_str(data)
    await user.send_json(data)


def get_app(argv=None):
    app = web.Application()
    app.add_routes(routes)
    return app


def passData():
    return _from


app = get_app()

# Adding Template files to the Project
aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates"))
)

# Adding Static files and folder to the Project.
# Ref:- https://github.com/aio-libs/aiohttp/blob/57df1d71a5322a599110bb4011ed7e28b28e6114/docs/web_advanced.rst
staticdir_ = os.path.join(os.getcwd(), "static")
cssdir_ = os.path.join(os.getcwd(), "static\css")
jsdir_ = os.path.join(os.getcwd(), "static\js")

app.add_routes([web.static('/static/', staticdir_)])
app.add_routes([web.static('/static/css/', cssdir_)])
app.add_routes([web.static('/static/js/', jsdir_)])

if __name__ == '__main__':
    ip = "192.168.1.18"
    # ip="127.0.0.1"
    web.run_app(app, host=ip, port=10000)
