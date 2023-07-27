# Primary Import Files
import asyncio
import base64
from cryptography import fernet
from cryptography.fernet import Fernet
from aiohttp import web, ClientSession
from aiohttp_session import setup, get_session, session_middleware
from aiohttp_session_mongo import MongoStorage
import motor.motor_asyncio as aiomotor
from aiohttp_session import *   
from aiohttp_session.cookie_storage import EncryptedCookieStorage


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

# Directory Import Files
# from chatlib import *
from common.commonFunctions import *

from Database.databaseConfig import *
from Database.databaseConfig import GroupList, Users, UserDetails, EmailVerification, Messages, websockets, test, workSpace, session_token
from SocketOnResponse.responseSocket import respondToSocket
from common.urls import *


routes = web.RouteTableDef()
# websockets = set()
# history = []
# test = {}


# Login/Home page Get Form
@routes.get(LOGIN_URL, name='hello')
async def hello(request):
    # workSpace = json.loads(request.cookies.get('CHAT_APP'))
    # workSpaceName = workSpace['session']['workSpaceName'] 
    context = {
        "workSpaceName": "workSpaceName",
    }
    response = aiohttp_jinja2.render_template("login.html", request,context=context)
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
@routes.get(SIGNUP_URL, name='signup')
async def signup_(request):
    context = {}
    response = aiohttp_jinja2.render_template("signup.html", request,context=context)
    return response


# SignUp Post Form
@routes.post(SIGNUP_URL, name='signup')
async def signup(request):
    user_data = await request.post()
    u_name = user_data.get('username')
    u_passw = user_data.get('password')
    email_Id = user_data.get('emailId')
    groupLink = user_data.get('groupLink')
    if not groupLink:
        otp = generateOtp()
        hashedpw = bcrypt.hashpw(u_passw.encode('utf-8'), bcrypt.gensalt())
        

        if SignupUserExist(u_name,email_Id):
            context = {
                "errno": "Username or Email I'd Already Exist's. Try diffrent Username or Email I'd"
            }
            response = aiohttp_jinja2.render_template("signup.html", request,context=context)
            return response
        else:
            context = {}
            response = aiohttp_jinja2.render_template("signup.html", request, context=context)
            EmailVerification.insert({"userName":u_name,"emailId": email_Id,"password":hashedpw,"verifyOtp":otp})
            mail_content = "Hello,Email verification mail enter the below OTP in your browser to verify.Your OTP is: " + otp + " Thank You."
            subject = 'One Time Password(OTP) for ChatApplication.'
            sendEmail(email_Id,mail_content,subject)
            new_user_Session = await new_session(request)
            new_user_Session['newUser'] = u_name
            raise web.HTTPFound(VERIFY_EMAIL_URL)
            
            return response
    else:
        print("Check workspace name is exist or not, then we have to check current user is invited by that workspace or not ")
    
@routes.get(VERIFY_EMAIL_URL)
async def verifyEmail_(request):
    try:
        cookie = json.loads(request.cookies.get('CHAT_APP'))
        name = cookie['session']['newUser']

        data = EmailVerification.find_one({"userName":name},{"_id":0})

        mail_context = {
            "userName":data['userName'],
            "emailId":data['emailId'],
            "password":data['password']
        }
        response = aiohttp_jinja2.render_template("emailVerification.html", request, context=mail_context)
        return response
    except:
        print("May error on /messenger/verifyemail")
        raise web.HTTPFound(ROOT)

@routes.post(VERIFY_EMAIL_URL)
async def verifyEmail(request):
    try:
        cookie = json.loads(request.cookies.get('CHAT_APP'))
        name = cookie['session']['newUser']

        data = EmailVerification.find_one({"userName":name},{"_id":0})

        mail_context = {
            "userName":data['userName'],
            "emailId":data['emailId'],
            "password":data['password']
        }
        verifyOtp = await request.post()
        user_otp = verifyOtp.get('otp')
        if  user_otp == data['verifyOtp']:
            
            # Activating Account.
            # Key Generation
            key = Fernet.generate_key()
            activateAccount(data['userName'], data['password'], key, data['emailId'])
            EmailVerification.delete_one({"userName":data['userName']})
            

            mail_context = {
                "errno":"User is Sucessfully created!!Please SignIn",
                "userName":data['userName']
            }
            response = aiohttp_jinja2.render_template("login.html", request, context=mail_context)
            return response
        else:
            context = {
                "errno": "Entered Otp is Wrong!. Check Your Entered Email for the OTP",
                "userName":data['userName'],
                "emailId":data['emailId'],
                "password":data['password']
            }
            response = aiohttp_jinja2.render_template("emailVerification.html", request, context=context)
            return response
    except:
        print("ERROR:May occur on /messenger/verifyEmail")
        raise web.HTTPFound(ROOT)



    response = aiohttp_jinja2.render_template("emailVerification.html", request, context=mail_context)
    return response



@routes.get(ROOT)
async def workspace_(request):
    try:
        cookie = json.loads(request.cookies.get('CHAT_APP'))['session']
        session = await get_session(request)
        last_visit = session['last_visit'] if 'last_visit' in session else None
    except:
        cookie = {}

    if checkKeyInDict('Token',cookie):
        raise web.HTTPFound(MAINPAGE_URL)
    else:
        mail_context = {}
        response = aiohttp_jinja2.render_template("workspace.html", request, context=mail_context)
        return response


@routes.post(ROOT)
async def _workspace(request):
    mail_context = {}
    data = await request.post()
    workSpaceName = data.get('workspace')

    if checkWorkSpace(workSpaceName):
        # session = await get_session(request)
        # session['workSpaceName'] = workSpaceName
        # workSpaceName = session['workSpaceName'] if 'workSpaceName' in session else None
        """
        Above code Update for the Using Of MONGO_SESSION instead of Normal AIOHTTP_SESSION cookies.
        Sample code for the AIOHTTP_SESSION is on Bellow.
        """
        workSpaceSession = await new_session(request)
        workSpaceSession['workSpaceName'] = workSpaceName
        raise web.HTTPFound(LOGIN_URL)
    else:
        mail_context = {
            "errno":"There is No Workspace with this Name. Kindly contact the Admin / Organization"
        }
        response = aiohttp_jinja2.render_template("workspace.html", request, context=mail_context)
        return response


# Login Post Form
@routes.post(LOGIN_URL)
async def login(request):
    form_data = await request.post()

    name = form_data.get('username')
    passw = form_data.get('password')

    if checkUserExist(name):
        if checkUserPass(name, passw):
            try:
                workSpace = json.loads(request.cookies.get('CHAT_APP'))
                workSpaceName = workSpace['session']['workSpaceName']
            except:
                session = await new_session(request)
                session['Token'] = generateToken(checkUserPass(name,passw))

                raise web.HTTPFound(GET_WORKSPACE_URL)

            session = await new_session(request)
            session['Token'] = generateToken(checkUserPass(name,passw))
            session['workSpaceName'] = workSpaceName
            raise web.HTTPFound(MAINPAGE_URL)
        else:
            loginContext = {
                "errno": "Username or Password Does'nt Match either!"
            }
            response = aiohttp_jinja2.render_template("login.html", request,
                                                      context=loginContext)
            return response
    else:
        context={
            "errno":"Invalid UserName! Please Signup!"
        }
        response = aiohttp_jinja2.render_template("login.html", request,context=context)
        return response

@routes.get(GET_WORKSPACE_URL)
async def getWorkSpace(request):
    cookie = json.loads(request.cookies.get('CHAT_APP'))
    Username = decryptToken(cookie['session']['Token'])
    context ={
        "userName":Username
    }
    response = aiohttp_jinja2.render_template("getWorkpace.html", request,context=context)
    return response

@routes.post(GET_WORKSPACE_URL)
async def getWorkSpace_(request):
    form_data = await request.post()
    workspace = form_data.get('workspace')
    cookie = json.loads(request.cookies.get('CHAT_APP'))
    if checkWorkSpace(workspace):
        session = await new_session(request)
        session['Token'] = cookie['session']['Token']
        session['workSpaceName'] = workspace
        raise web.HTTPFound(MAINPAGE_URL)
    else:
        context ={
        "errno":"Entered workspace is wrong. Please enter the right Workplace."
        }
        response = aiohttp_jinja2.render_template("getWorkpace.html", request,context=context)
        return response


@routes.get(WEBSOCKET_URL)
async def websocket(request):
    cookie = json.loads(request.cookies.get('CHAT_APP'))
    name = decryptToken(cookie['session']['Token'])
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    data = active_users.find_one({"username":name})
    if data is not None:
        pass
    else:
        active_users.insert({"username":name})
    # print(name + "online!")

    for text in list(history):
        await ws.send_json(text)
    websockets.add(ws)
    test[name] = ws

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                MessageData = json.loads(msg.data)
                await respondToSocket(MessageData)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())
    finally:
        websockets.remove(ws)
        active_users.delete_one({"username":name})
    # print(name + "left")

    return ws


@routes.get(MAINPAGE_URL, name='chat')
async def chat_page(request):
    try:
        cookie = json.loads(request.cookies.get('CHAT_APP'))
        Username = decryptToken(cookie['session']['Token'])
        workSpaceName = cookie['session']['workSpaceName']
        workspaces = getWorkSpaces(Username)

        from workSpace.createWorkSpace import getUserListForWorkspace, createWorkspace, new_getGroupListForWorkspace
        if Username in getUserListForWorkspace(workSpaceName):
            userList = getUserListForWorkspace(workSpaceName)
            groups = new_getGroupListForWorkspace(Username,workSpaceName)
            Mess = retriveOlderMessage(Username, userList, groups, workSpaceName)
            groupmembers = []
            for g in groups:
                g_data = g,getGroupMembers_Workspace(g,workSpaceName)
                groupmembers.append(g_data)
            
            workSpaceMembers = getWorkspaceMembers(workSpaceName)

            context = {
                'Users': userList,
                'Groups': groups,
                'userName': Username,
                'Messages': Mess,
                'workSpaceName':workSpaceName,
                'groupmembers': groupmembers,
                'workSpaceMembers': workSpaceMembers,
                'workspaces':workspaces
            }

            response = aiohttp_jinja2.render_template("index.html", request,
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
        else:
            loginContext = {
                "errno": "Unauthorized User! you were not a member of the WorkSpace.PLease kindly contact Admin."
            }
            response = aiohttp_jinja2.render_template("login.html", request,
                                                      context=loginContext)
            return response
    except:
        print("May Error on /messenger/mainPage")
        context={
        }
        response = aiohttp_jinja2.render_template("workSpace.html", request,context=context)
        return response



# EditProfile
@routes.get(EDIT_PROFILE_URL)
async def editprofile(request):
    cookie = json.loads(request.cookies.get('CHAT_APP'))
    Username = decryptToken(cookie['session']['Token'])

    if Username in getTotalUserList():
        context = {
            'Username': Username,
        }
        response = aiohttp_jinja2.render_template("profile.html", request,
                                                  context=context)
        return response
    else:
        raise Exception("Unauthorized User")


@routes.get(CREATE_WORKSPACE_URL)
async def _createWorkSpace(request):
    try:
        LogUser = json.loads(request.cookies.get('CHAT_APP'))
        try:    
            Username = decryptToken(LogUser['session']['Token'])
        except:
            Username = LogUser['session']['newUser']
        context = {
            "userName":Username
        }
        response = aiohttp_jinja2.render_template("createWorkSpace.html", request,context=context)
        return response
    except :
        context={
            "errno":"User is Not Logged In! Please Login First and try Creating Workspace."
        }
        response = aiohttp_jinja2.render_template("login.html", request, context=context)        
        return response


@routes.post(CREATE_WORKSPACE_URL)
async def createWorkSpace_(request):
    createWorkSpaceData = await request.post()
    workSpaceName = createWorkSpaceData.get('workSpaceName')
    userName = createWorkSpaceData.get('userName')
    description = createWorkSpaceData.get('description')

    if userName in getTotalUserList():
        from workSpace.createWorkSpace import createWorkspace
        createWorkspace(workSpaceName,userName,description)
        Messages.insert({"userId":getUserID(userName),"User":userName,"workSpaceName":workSpaceName})
        try:
            load = json.loads(request.cookies.get('CHAT_APP'))
        except:
            pass
        
        session = await new_session(request)
        session['Token'] = load['session']['Token']
        session['workSpaceName'] = workSpaceName
        raise web.HTTPFound(ROOT)
    else:
        print("Invalid Username! Please enter correct username or Signup!")
        context={
            "errno":"Invalid Username! Please enter correct username or Signup!"
        }
        response = aiohttp_jinja2.render_template("error.html", request,context=context)
        return response

def getUserListForWorkspace(workSpaceName):
    try:
        return [getUserName(temp) for temp in workSpace.find_one({"workSpaceName":workSpaceName},{"_id":0,"users":1})['users']]
    except:
        return "error:on getUserListForWorkspace()[line:316,file:chat.py]"


@routes.get(FILEUPLOAD_URL)
async def _fileUpload(request):
    context = {}
    
    response = aiohttp_jinja2.render_template("emoji.html", request,context=context)
    return response

@routes.post("/messenger/userOnGroup")
async def _fileUpload(request):
    createWorkSpaceData = await request.post()
    workSpaceName = createWorkSpaceData.get('workSpaceName')
    userName = createWorkSpaceData.get('userName')
    groupName = createWorkSpaceData.get('groupName')
    userId = getUserID(userName) 
    
    if userName in getGroupMembers_Workspace(groupName,workSpaceName):
        return web.Response(text=json.dumps({"userId":userId,"userName":userName,"ismember":True}))
    else:
        return web.Response(text=json.dumps({"userId":userId,"userName":userName,"ismember":False}))

@routes.get(LOGOUT_URL)
async def logout(request):
    cookie = json.loads(request.cookies.get('CHAT_APP'))
    name = decryptToken(cookie['session']['Token'])
    
    cookie['session'] = {}
    logout_session = await new_session(request)
    logout_session['task'] ="logged Out sucessfully"
    print(logout_session)
    # logout_context = {
    #     "errno":"User Logged out Sucessfully!!"
    # } 
    # response = aiohttp_jinja2.render_template("workspace.html", request, context=logout_context)
    # return response
    raise web.HTTPFound(ROOT)

@routes.post(SWITCH_WORKPLACE_URL)
async def _fileUpload(request):
    createWorkSpaceData = await request.post()
    workSpaceName = createWorkSpaceData.get('workSpaceName')
    
    LogUser = json.loads(request.cookies.get('CHAT_APP'))
    switchSession = await new_session(request)
    switchSession['Token'] = LogUser['session']['Token']
    switchSession['workSpaceName'] = workSpaceName

    raise web.HTTPFound(MAINPAGE_URL)

@routes.post(FILEUPLOAD_URL)
async def store_file_handler(request):
    try:
        reader = await request.multipart()
        
        r = await reader.next() # <-- Critical Error here#
        filename = r.filename

        size = 0
        path = './static/files'
        with open(os.path.join(path, filename), 'wb') as f:
            while True:
                chunk = await r.read_chunk()
                if not chunk:
                    break
                size += len(chunk)
                f.write(chunk)

        return web.HTTPNoContent()
    except:
        print(
            "try changing the Web_Exceptions.py `class HTTPNoContent(HTTPSuccessful):` commment the line ''EmptyBody=true'' "
            )
        
        raise web.HTTPFound(MAINPAGE_URL)


@routes.get(INVITE_URL)
async def invitation_handler(request):
    try:
        token = request.match_info.get('name', "Anonymous")
        from common.commonFunctions import decryptInviteToken
        data = decryptInviteToken(token)

        text = "You have been invited to chatApp using Invitation link,for the {} workSpace".format(data['workSpaceName'])
        switchSession = await new_session(request)
        switchSession['workSpaceName'] = data['workSpaceName']
        mail_context = {
            "errno": text
        }
        response = aiohttp_jinja2.render_template("login.html", request, context=mail_context)
        return response

    except IndexError as e:
        return web.Response(text="excepion block")


@routes.get(INVITE_USER_URL)
async def invitation_handler(request):
    try:
        token = request.match_info.get('name', "Anonymous")
        from common.commonFunctions import decryptInviteToken
        data = decryptInviteToken(token)

        text = "You have been invited to chatApp using Invitation link,for the {} workSpace".format(data['workSpaceName'])
        switchSession = await new_session(request)
        switchSession['workSpaceName'] = data['workSpaceName']
        mail_context = {
            "errno": text
        }
        response = aiohttp_jinja2.render_template("signup.html", request, context=mail_context)
        return response

    except IndexError as e:
        return web.Response(text="excepion block")


@routes.get(ACCOUNT_RECOVERY_URL)
async def accountRecovery(request):
    mail_context = {}
    response = aiohttp_jinja2.render_template("AccountRecovery.html", request, context=mail_context)
    return response


@routes.post(ACCOUNT_RECOVERY_URL)
async def accountRecovery(request):
    Account = await request.post()
    id = Account.get('AccountID')
    Data = recoverAccount(id)
    
    import datetime
    NOW = datetime.datetime.utcnow()
    
    key = Fernet.generate_key() 
    
    session_token.insert({"createdAt":NOW,"Token":key.decode('utf-8'),"userName":Data['User'],"EmailId":Data['EmailId']})
    url_ = "http://192.168.1.18:10000/messenger/reset/account/"+key.decode('utf-8')
    mail_content = "Hello,PLease click the bellow link to reset the account Password. This Link will be only valid for 2 minutes.\n "+url_
    subject = 'Change Password for account.'
    sendEmail(Data['EmailId'],mail_content,subject)

    mail_context = {
        "errno": "Password Reset link has sent to Your Registered Email Id"
    }
    response = aiohttp_jinja2.render_template("workSpace.html", request, context=mail_context)
    return response


@routes.get(PASS_RESET_URL)
async def _urlReset(request):
    token = request.match_info.get('token', "None")
    session = await new_session(request)
    session['Token'] = token
    data = session_token.find_one({"Token":token},{"_id":0,"createdAt":0})
    if data is None:
        mail_context = {
            "errno": "your Link has Expired. Please Try Again!."
        }
        response = aiohttp_jinja2.render_template("login.html", request, context=mail_context)
        return response
    else:
        mail_context = {}
        response = aiohttp_jinja2.render_template("password_correction.html", request, context=mail_context)
        return response


@routes.post(PASS_RESET_URL)
async def urlReset_(request):
    LogUser = json.loads(request.cookies.get('CHAT_APP'))
    token = LogUser['session']['Token']
    data = session_token.find_one({"Token":token},{"_id":0,"createdAt":0})
    Pass_ = await request.post()
    New_Pass = Pass_.get('newPassword')
    Renter_Pass = Pass_.get('reEnterPassword')
    if data is not None:
        if New_Pass == Renter_Pass:
            hashedpw = bcrypt.hashpw(New_Pass.encode('utf-8'), bcrypt.gensalt())
            Users.update_one({"username":data['userName']},{"$set":{"password":hashedpw}}) 
            mail_context = {
                "errno": "Password has changed Sucessfully please Login again!"
            }
            response = aiohttp_jinja2.render_template("login.html", request, context=mail_context)
            return response
        else:
            mail_context = {
                "errno": "Passwords Doesn't match either!."
            }
            response = aiohttp_jinja2.render_template("password_correction.html", request, context=mail_context)
            return response
    else:
        mail_context = {
            "errno": "your Link has Expired. Please Try Again!."
        }
        response = aiohttp_jinja2.render_template("login.html", request, context=mail_context)
        return response

@routes.get("/messenger/test")
async def _fileUpload(request):
    context = {}
    
    response = aiohttp_jinja2.render_template("test.html", request,context=context)
    return response

def get_app(argv=None):
    app = web.Application()
    setup(app, SimpleCookieStorage(cookie_name="CHAT_APP"))
    app.add_routes(routes)
    return app


app = get_app()

# Adding Template files to the Project
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))

# Adding Static files and folder to the Project.
# Ref:- https://github.com/aio-libs/aiohttp/blob/57df1d71a5322a599110bb4011ed7e28b28e6114/docs/web_advanced.rst
staticdir_ = os.path.join(os.getcwd(), "static")
ckeditor = os.path.join(os.getcwd(), "ckeditor")
cssdir_ = os.path.join(os.getcwd(), "static\css")
jsdir_ = os.path.join(os.getcwd(), "static\js")
filesdir_ = os.path.join(os.getcwd(), "static\\files")

app.add_routes([web.static('/messenger/static/', staticdir_)])
app.add_routes([web.static('/messenger/ckeditor/', ckeditor)])
app.add_routes([web.static('/messenger/static/css/', cssdir_)])
app.add_routes([web.static('/messenger/static/js/', jsdir_)])
app.add_routes([web.static('/messenger/static/files/', filesdir_)])



# if __name__ == '__main__':
#     ip = "192.168.1.18"
#     # ip="127.0.0.1"
    # web.run_app(app, host=ip, port=10000)
