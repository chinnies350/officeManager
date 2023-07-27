from Database.databaseConfig import *
from Database.databaseConfig import GroupList, Users, UserDetails, EmailVerification, Messages, test, websockets, workSpace, active_users, session_token

import asyncio
from .test import *
from common.commonFunctions import *
from common.sendMessages import send_to_all,send_to_user
from workSpace.createWorkSpace import getUserListForWorkspace, new_getGroupListForWorkspace, createWorkspace 


async def respondToSocket(MessageData):

    if MessageData['task'] == "onMessage":
        global toUser, Message, _from
        toUser, Message, _from = decrypt(MessageData)

        from Database.storeMessages import storeMessageToDatabase
        storeMessageToDatabase(_from, toUser, Message, MessageData['workSpaceName'],MessageData['type_'], MessageData)
        
        """
        Checks the User Based on the Messages Included Try Except Block if the User Sends the Message to
        the Invalid User Websockets getting Closed. TRY EXCEPT prevents from the Websockets close.
        the Message might append on the Frontend but will be Received on the Other User.
        """

        try:
            from SocketOnResponse.test import getCurrentTime
            date_time = getCurrentTime()
            await send_to_user(_from, toUser, test[toUser], Message, MessageData['type_'],MessageData,date_time)
        except KeyError:
            try:
                if _from in getGroupMembers(toUser):
                    await send_to_all(_from, toUser, Message, getGroupMembers(toUser),MessageData['type_'],MessageData)
                else:
                    print("user might be offline or invalid groupName")
            except KeyError:
                print("Invalid ID! But The Message will be Appended")

    elif MessageData['task'] == "createGroup":
        from common.commonFunctions import createGroup
        createGroup(MessageData)
        workSpace.update_one({"workSpaceName":MessageData['workSpaceName']},{"$push":{"GroupList":MessageData['groupName']}})
        alertMessage = "Group Created!"
        await alertUser(test[MessageData['Admin']], alertMessage)

    elif MessageData['task'] == "retrieveOlderMessage":
        userList = getUserListForWorkspace(MessageData['workSpaceName'])
        groups = new_getGroupListForWorkspace(MessageData['From'],MessageData['workSpaceName'])
        from common.commonFunctions import  retriveOlderMessage
        olderMessage = retriveOlderMessage(MessageData['From'],userList,groups,MessageData['workSpaceName'])
        retrieveOlderMessage = {"task": "retriveOlderMessage", "data": olderMessage}
        requestedUser = test[MessageData['From']]
        # print(retrieveOlderMessage,requestedUser)
        await requestedUser.send_json(retrieveOlderMessage)

    elif MessageData['task'] == "addUserToGroup":
        try:
            if checkUserExist(MessageData['addUserName']):
                await addUserToGroup(MessageData)
            else:
                alertMessage = "Invalid Username or User must already exist!"
                await alertUser(test[MessageData['requestingUser']], alertMessage)
        except:
            alertMessage = "Only Admins can Add User to the group.We have Notified Admin To Add " + \
                MessageData['addUserName'] + " to the group"
            await alertUser(test[MessageData['requestingUser']], alertMessage)

    elif MessageData['task'] == "editProfile":
        editProfile(MessageData)
    
    elif MessageData['task'] == "emailVerification":
        emailVerification(MessageData['emailId'])
    
    elif MessageData['task'] == "addUserToWorkSpace":
        try:
            _idUser = UserDetails.find_one({"EmailId":MessageData['addUserMail']},{"_id":0,"userId":1})['userId']
            print("found")
            # {'task': 'addUserToWorkSpace', 'requestingUser': 'beast', 'workSpaceName': 'android', 'addUserMail': 'mohanpandi07@gmail.com'}
            if workSpace.find_one({"workSpaceName":MessageData['workSpaceName'],"users":_idUser}) == None:
                workSpace.update_one({"workSpaceName":MessageData['workSpaceName']},{"$push":{"users":_idUser}})
                
                from common.commonFunctions import encryptInviteToken
                token = encryptInviteToken(MessageData['workSpaceName'],MessageData['requestingUser'])
                url_ = "http://192.168.1.18:10000/messenger/invite/"+token

                from common.commonFunctions import sendEmail
                mail_content = "Dear User,\n Welcome To ChatApp."+ MessageData['requestingUser'] +" has Invited you to the "+ MessageData['workSpaceName'] +" Group!. Please click bellow Link.{}"
                mail_content = mail_content.format(url_)
                
                subject = "Notification: "+ MessageData['requestingUser'] +" Invited you to the "+ MessageData['workSpaceName'] +" Group!"
                sendEmail(MessageData['addUserMail'],mail_content,subject)
                from common.commonFunctions import getUserName
                Messages.insert({"userId":_idUser,"User":getUserName(_idUser),"workSpaceName":MessageData['workSpaceName']})
                alertMessage = "User Added to the WorkSpace"
                await alertUser(test[MessageData['requestingUser']], alertMessage)
            else:
                alertMessage = "User is already in Workspace!"
                await alertUser(test[MessageData['requestingUser']], alertMessage)
        except:
            from common.commonFunctions import sendEmail
            print("May Exception on Inviting Email SMTP server")
            
            from common.commonFunctions import encryptInviteToken
            token = encryptInviteToken(MessageData['workSpaceName'],MessageData['requestingUser'])
            url_ = "http://192.168.1.18:10000/messenger/invite-user/"+token

            mail_content = "Dear User,\n Welcome To ChatApp."+ MessageData['requestingUser'] +" has Invited you to the "+ MessageData['workSpaceName'] +" Group!. Please click bellow Link & signup to Use the Workspace.The bellow link will be valid only for 15 Minutes.\n"+url_
            mail_content = mail_content.format(url_)

            subject = "Notification: "+ MessageData['requestingUser'] +" Invited you to the "+ MessageData['workSpaceName'] +" Group!"
            
            import datetime
            NOW = datetime.datetime.utcnow()
            session_token.insert({"createdAt":NOW,"Token":token,"EmailId":MessageData['addUserMail'],"workSpaceName":MessageData['workSpaceName']})
            
            sendEmail(MessageData['addUserMail'],mail_content,subject)
            alertMessage = "Notification has    Sent to the User!"
            await alertUser(test[MessageData['requestingUser']], alertMessage)
    
    elif MessageData['task'] == "activeUsers":
        # {'task': 'activeUsers', 'requestingUser': 'beast', 'workSpaceName': 'python'}
        from common.commonFunctions import getUserName
        workSpaceUsers = [getUserName(temp) for temp in workSpace.find_one({"workSpaceName":MessageData['workSpaceName']},{"_id":0,"users":1})["users"]]
        activeUsers = [temp['username'] for temp in active_users.find()]
        online = []
        offline = []
        for user in workSpaceUsers:
            if user in activeUsers:
                online.append(user)
            else:
                offline.append(user)
        
        activeUsers_ = {"task": "activeUsers","online":online,"offline":offline}
        requestedUser = test[MessageData['requestingUser']]
        await requestedUser.send_json(activeUsers_)
        