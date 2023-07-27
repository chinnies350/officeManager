"""
versio:1.0
This is the complete Application Library For all the specific Functions of the Chat Application.
Lastedit - Beast - 5/11/20
"""

import random
import math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
from pymongo import MongoClient
import bcrypt
from chat import *
import json
from datetime import datetime
from groupChat import *
from cryptography.fernet import Fernet

from Database.databaseConfig import *
from Database.databaseConfig import GroupList, Users, UserDetails, EmailVerification, Messages 


# Get UserID for Username
def getUserID(userName):
    return Users.find_one({"username": userName}, {"_id": 0, "userId": 1})['userId']

# Get total Users List.


def getTotalUserList():
    return [temp['username'] for temp in Users.find({}, {"_id": 0, "username": 1})]


# Generate GroupMessage Id.
def createGroupMessageId(groupName):
    try:
        return [temp['messageId'] for temp in GroupList.find_one({"groupName": groupName}, {"_id": 0, "Messages": 1})['Messages']][-1]
    except:
        return 1


# Create the Specific UserId For each users.
def createUserId():
    try:
        return [temp['userId'] for temp in Users.find({}, {"_id": 0, "userId": 1})][-1:][0] + 1
    except:
        return 1


# Activates Acount by initializing all the Possible Database collections.
def activateAccount(u_name, hashedpw, key):
    try:
        uId = createUserId()
    except:
        uId = 1
    Users.insert({'userId': uId, 'username': u_name,
                 'Key': key, 'password': hashedpw})
    Messages.insert({'userId': uId, "User": u_name})
    UserDetails.insert({'userId': uId, "User": u_name,
                        "EmailId": "", "phoneNo": "", "jobDetails": "", "ChatList": [], "GroupList": []})


# Get Current time For Message time
def getCurrentTime():
    return datetime.now().strftime("%H:%M:%S")


# checking the user existence on the database
def checkUserExist(username):
    if Users.find({"username": username}).count() > 0:
        return True
    else:
        return False

# Get UserName for UserID


def getUserName(userId):
    return Users.find_one({"userId": userId}, {"_id": 0, "username": 1})["username"]

# Get Specific Group Admin.


def getGroupAdmin(groupName):
    return getUserName(GroupList.find_one({"groupName": {"$eq": groupName}}, {"_id": 0, "Admin": 1})['Admin'])

# Adding User to the Group.


def addUserToGroup(_request_):
    if _request_['requestingUser'] == getGroupAdmin(_request_['groupName']):
        UserDetails.update({"User": _request_['addUserName']}, {
                           "$push": {"GroupList": _request_['groupName']}})
        GroupList.update({"groupName": _request_['groupName']}, {
                         "$push": {"Users": getUserID(_request_['addUserName'])}})
    else:
        raise Exception("Only admin can Add members to group")


# Initialize the Group
def createGroup(_request_):
    GroupList.insert({"groupName": _request_['groupName'], "Admin": getUserID(
        _request_['Admin']), "Users": [getUserID(_request_['Admin'])], "Messages": []})
    UserDetails.update({"User": _request_['Admin']}, {
                       "$push": {"GroupList": _request_['groupName']}})


# Getting the User pass for the Authentication.
def checkUserPass(username, password):
    try:
        hashed_pw = Users.find({"username": username})[0]["password"]
    except:
        Uname = UserDetails.find_one({"EmailId": username}, {
                                     "_id": 0, "User": 1})['User']
        hashed_pw = Users.find({"username": Uname})[0]["password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False


# Decrypt message
def decrypt(msg):
    msg_decrypt = msg
    toUser = msg_decrypt['To']
    privateMessage = msg_decrypt['message']
    _from = msg_decrypt['From']

    return toUser, privateMessage, _from


# Getting the Total Userlist
def getUserListForUser(userName):
    try:
        return UserDetails.find_one({'User': userName}, {"_id": 0, "ChatList": 1})['ChatList']
    except:
        return []


# Alert User
async def alertUser(toUser, alertMessage):
    flash_message = {"task": "flash", "alertMessage": alertMessage}
    await toUser.send_json(flash_message)


# Getting the Total Grouplist
def getGroupListForUser(userName):
    try:
        return UserDetails.find_one({'User': userName}, {"_id": 0, "GroupList": 1})['GroupList']
    except:
        return []

# Get Total GroupList


def getTotalGroupList():
    return [temp['groupName'] for temp in GroupList.find({}, {"_id": 0, "groupName": 1})]


# Get Total group members in a Group.
def getGroupMembers(groupName):
    try:
        return [getUserName(temp) for temp in GroupList.find_one({"groupName": groupName}, {"_id": 0, "Users": 1})['Users']]
    except:
        return []


# Retrieving Older Messages.
def retriveOlderMessage(userName):
    try:
        doc = Messages.find_one({'User':
                                {"$eq": userName}}, {
            "_id": 0, "User": 0, "userId": 0})
        oldmsg = []

        # For Private Message
        for eachUser in doc:
            messageData = eachUser, doc[eachUser][-9:]
            oldmsg.append(messageData)

        # For Group Message
        for grpName in UserDetails.find_one({"User": userName}, {"_id": 0, "GroupList": 1})['GroupList']:
            groupMessageData = GroupList.find_one(
                {"groupName": grpName}, {"_id": 0, "Messages": 1})['Messages'][-9:]
            for temp in groupMessageData:
                temp['from'] = getUserName(temp['from'])

            oldmsg.append((grpName, groupMessageData))

        return oldmsg
    except:
        return 0


def editProfile(messageData):
    myquery = {"User": {"$eq": messageData['requestingUser']}}
    newvalues = {"$set": {"User": messageData['userName'],
                          "EmailId": messageData['emailId'], "phoneNo": messageData['phoneNumber'], "jobDetails": messageData['jobDetails']}}
    x = UserDetails.update_many(myquery, newvalues)
    return x


def getUserByEmail(userName):
    pass


def getKey(userName):
    return Users.find_one({"username": userName}, {"_id": 0, "Key": 1})['Key']


def generateToken(userName):
    _token = getKey(userName).decode('utf-8')
    cipher_suite = Fernet(getKey(userName))
    token_ = cipher_suite.encrypt(userName.encode('utf-8'))
    T = _token+","+token_.decode('utf-8')
    return T



def decryptToken(Token):
    token = Token.split(",")
    _T = token[0].encode('utf-8')
    cipher_suite = Fernet(_T)
    toDecrypt = token[1].encode('utf-8')
    return cipher_suite.decrypt(toDecrypt).decode('utf-8')


def generateOtp():
    digits = "0123456789"
    OTP = ""
    for i in range(4):
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


def Og(emailId):
    if emailId.find("gmail") == -1:
        return False
    else:
        return True


def emailVerification(emailId, otp):

    mail_content = "Hello,Email verification mail enter the below OTP in your browser to verify.Your OTP is: " + otp + " Thank You."
    # The mail addresses and password
    sender_address = 'chatapplication321@gmail.com'
    sender_pass = 'Chatapplication@123'
    receiver_address = emailId
    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'One Time Password(OTP) for ChatApplication.'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()


def checkEmailId(emailId):
    if UserDetails.find_one({"EmailId": emailId}, {"_id": 0}):
        return True
    else:
        return False
