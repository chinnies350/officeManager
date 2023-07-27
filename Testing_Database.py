from pymongo import MongoClient
# from chatlib import *
import hashlib
from Groupchat.sendGroup import printGroup
from Database.databaseConfig import GroupList, Users, UserDetails, EmailVerification, Messages, websockets, test, workSpace,active_users, session_token
from cryptography.fernet import Fernet

from datetime import datetime
import time
def getCurrentTime():
    return datetime.now().strftime("%I:%M %p"),time.strftime("%d/%m/%Y")

from common.commonFunctions import getUserName


# def getGroupListForWorkspace(username,workSpaceName):
#     try:
#         g = []
#         groups_ = workSpace.find_one({"workSpaceName":workSpaceName},{"_id":0,"GroupList":1})['GroupList']
#         for group in groups_:
#             userlist = [getUserName(temp) for temp in GroupList.find_one({"workSpaceName":workSpaceName,"groupName":group},{"_id":0,"Users":1})['Users']]
#             if username in userlist:
#                 g.append(group)
#         return g
#     except:
#         return "wrong with getting grouplist"

# print(getGroupListForWorkspace("fgsdf","pyhon"))
print(session_token.find_one({"EmailId":"mraja1788@gmail.com"},{"_id":0,"EmailId":1,"workSpaceName":1}))



# import datetime
# NOW = datetime.datetime.utcnow()
# print(NOW)
# session_token.insert({"createdAt":NOW,"Token":"SDgszfgfd"})



# username_ = "beast"
# workspace_ = "python"
# c = username_+","+workspace_
# # print(c)

# key = Fernet.generate_key()
# f = Fernet(key) 
# token = f.encrypt(b"python,beast") 
# # print(token.decode('utf-8'),key)
# d = f.decrypt(token)
# # print(d.decode('utf-8'))

# from common.commonFunctions import encryptInviteToken
# token = encryptInviteToken("python","beast")
# url = "http://192.168.1.18:10000/invite/"
# link = str(url).concat(token)
# print(link)

# # Database connection
# client = MongoClient('mongodb://192.168.1.221:27017/')
# db = client.MadhukaranDb
# # db = client.akshayaDB
# # col = db['hotel_booking_chat']
# user = db['Users']
# messages = db['Messages']
# groupList = db['GroupList']
# UserDetails = db['UserDetails']
# workSpace = db['workSpace']

from common.commonFunctions import checkWorkSpace
# from workSpace.createWorkSpace import getUserListForWorkspace, getGroupListForWorkspace, createWorkspace

from common.commonFunctions import getGroupMembers
# print(getGroupMembers("test"))
from common.commonFunctions import getTotalUserList



# print(col.find_one({}))

# col.update_one({"chatId":1},{"$push":{"ChatHistory":{"userQuery":"test","Botresponse":"test"}}})

# col.insert({"chatId":1,"lastIntent":"B-Hotel","ModelIntent":"B-Hotel","IntentValue":"","ChatHistory":[]})
# data = {"ChatHistory":{"UserQuery":"testquery","Botresponse":"test"}}
# col.update_one({"chatId":1},{"$push":data})

# print(UserDetails.find_one({"EmailId":"madhukaran449@gmail.com"},{"_id":0,"User":1})['User'])




# from cryptography.fernet import Fernet

# key = Fernet.generate_key() #this is your "password"
# cipher_suite = Fernet(key)
# # print(key)
# encoded_text = cipher_suite.encrypt(b'beast')
# decoded_text = cipher_suite.decrypt(encoded_text)
# # print(encoded_text)
# # print(decoded_text)

# token = generateToken("beast") 
# # print(token)
# # print(decryptToken(token))
# # print(decryptToken(token))

# def editProfile(userName):
#     myquery = {"User": {"$eq": userName}}
#     newvalues = {"$set": {"User": "mohan1"}}

#     UserDetails.update_many(myquery, newvalues)



# print(getUserID("beast"))
# print(getGroupMessage("beast"))
# for grpName in UserDetails.find_one({"User": "beast"}, {"_id": 0, "GroupList": 1})['GroupList']:
#     data = groupList.find_one({"groupName": grpName}, {"_id": 0, "Messages": 1})[
#         'Messages'][-9:]
#     for temp in data:
#         temp['from'] = getUserName(temp['from'])
#     # print((grpName,data))
    # print("*" * 100)


# print(user.find_one({"_id":ObjectId("5f9ff847052ebbd211aa4870")},{"_id":1,"username":1}))
# print(createGroupMessageId("test") + 1)
# print(getUserID("mohan"))
# print(getTotalUserList())
# print(getUserName(getUserID("mohan")))
# print(getGroupAdmin("android"))
# print(getGroupMembers("test"))
# print([temp['messageId'] for temp in groupList.find_one({"groupName":"test"},{"_id":0,"Messages":1})['Messages']][-1] + 1)
# print([temp['userId'] for temp in user.find({},{"_id":0,"userId":1})][-1] + 1)
# print(user.find_one({"userId":1},{"_id":0,"username":1})["username"])
# print(getUserID("beast"))
# def getLastUserId():
#     itm = userList.find({})
#     for i in itm:
#         x = i['userId']

#     return x

# val = "<WebSocketResponse Switching Protocols GET /beast/ws/ >"
# groupList.update({"groupName":"android"},{"$push":{"Users":val}})

# name = "Android"
# var = groupList.find_one({"groupName": {"$eq": name}}, {"_id": 0, "Admin": 1})
# print(var)

# user = "beast"
# var1 = UserDetails.find_one(
#     {'Name': user}, {"_id": 0, "GroupList": 1})['GroupList']
# var2 = UserDetails.find_one(
#     {'Name': user}, {"_id": 0, "ChatList": 1})['ChatList']
# print(var2)

# for temp in groupList.find({},{"_id":0,"groupName":1}):
# print(temp['groupName'])

# var3 = [temp['groupName']
#         for temp in groupList.find({}, {"_id": 0, "groupName": 1})]
# # print(var3)


# def getTotalGroupList():
#     return [temp['groupName'] for temp in groupList.find({}, {"_id": 0, "groupName": 1})]
# # print(getTotalGroupList())


# def getGroupMembers(groupName):
#     return groupList.find_one({"groupName": groupName}, {"_id": 0, "Users": 1})['Users']

# # print(getGroupMembers("Prematix_Test1"))


# def getGroupListForUser(userName):
#     return UserDetails.find_one({'Name': userName}, {"_id": 0, "GroupList": 1})['GroupList']


# # print(getGroupListForUser("dhana"))

# groupName = "Android"
# username = "beast"
# # UserDetails.update({"Name":username},{"$push": {"GroupList":groupName}})

# # print(UserDetails.find_one({'User':"beast"}, {"_id": 0, "ChatList": 1})['ChatList'])
# # var = message.find_one({"User":{"$eq":"beast"}},{"_id":0})
# # message.update({"User":"mohan"}, {"$push":{"mohan":{"beast":"dssfdbsf"}}})

# # def getmessage():
# #     mess = mess

# # db.Users.find({}).sort({_id:-1}).limit(1)

# # def retriveMessage(name):
# #     doc = message.find_one({'User': {"$eq": name}}, {
# #         "_id": 0, "User": 0, "userId": 0})
# #     oldmsg = []
# #     for eachUser in doc:
# #         messageData = eachUser, doc[eachUser][-10:]
# #         oldmsg.append(messageData)
# #     return oldmsg

# # mess = retriveMessage("beast")

# # for data in retriveMessage("beast"):
# #     if data[0] == "mohan":
# #         for msg in data[1]:
# #             print(msg['Message'])

# # def storemessage(_from, to, message):
# # var = message.find_one({"users":{"$eq":_from+to}},{"_id":0})
# # var_ = message.find_one({"users":{"$eq":to+_from}},{"_id":0})
# # print(var_, var)

# # def storemessage(_from, to, message):
# #     str_ = str(_from+to)
# #     var = message.find_one({"users":{"$eq":str_}},{"_id":0})
# #     print(var)

# # def storemessage(_from, to, message):
# # _var = message.find_one({"User":{"$eq":_from}},{"_id":0})
# # var_ = message.find_one({"User":{"$eq":to}},{"_id":0})
# # print(_var)

# # if _var == None:
# #     if var_ == None:
# #         # Testing.insert({"users" : _from+to,"messages" : []})
# #         # Testing.update({'users': to+_from}, {'$push': {'messages':{_from: message}}})
# #         print("creating Doc")
# #     else:
# #         # Testing.update({'users': to+_from}, {'$push': {'messages':{_from: message}}})
# #         print("creating if")
# # else:
#     print("creating else")


# def storemessage(_from, to, message):
# Testing.insert({"users" : _from+to,"messages" : []})
# Testing.update({'users': to+_from}, {'$push': {'messages':{_from: message}}})
#     Testing.update({'users': _from+to}, {'$push': {'messages':{_from : message}}})

#     try:

# for data in var:
#     users = data
#     if users == "Null":
#         print("null")
#         for dt in data['messages']:
#             for key,value in dt.items():
#                 # print(key, value)
#                 pass

# Testing.update({'users': to+_from}, {'$push': {'messages':{_from: message}}})
# Testing.update({'users': _from+to}, {'$push': {'messages':{_from : message}}})

# storemessage("beast","mohan","message")
