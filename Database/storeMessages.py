from . databaseConfig import *
from . databaseConfig import  GroupList, Messages
from SocketOnResponse.test import getTotalGroupList,getUserID,getCurrentTime


# storing Message to Database
def storeMessageToDatabase(_from,toUser,Message, workSpaceName, type_, MessageData):
    if type_ == "message":
        if toUser in getTotalGroupList():
            # print(_from, toUser, Message)
            GroupList.update_one({"groupName": toUser,"workSpaceName":workSpaceName}, {"$push": {"Messages": {"from": getUserID(_from), "Message": Message, "time": getCurrentTime()[0],"date": getCurrentTime()[1], "msgType": "R", "ReadStatus": "True","type_":type_}}})
        elif _from == toUser:
            Messages.update_one({"User": _from,"workSpaceName":workSpaceName}, {"$push": {toUser: {"Message": Message, "time": getCurrentTime()[0],"date": getCurrentTime()[1], "msgType": "S", "ReadStatus": "True","type_":type_}}})
        else:
            Messages.update_one({"User": _from,"workSpaceName":workSpaceName}, {"$push": {toUser: {
                                "Message": Message, "time": getCurrentTime()[0],"date": getCurrentTime()[1], "msgType": "S", "ReadStatus": "True","type_":type_}}})
            Messages.update_one({"User": toUser,"workSpaceName":workSpaceName}, {"$push": {_from: {
                                "Message": Message, "time": getCurrentTime()[0],"date": getCurrentTime()[1], "msgType": "R", "ReadStatus": "True","type_":type_}}})
    else:
        if toUser in getTotalGroupList():
            GroupList.update_one({"groupName": toUser,"workSpaceName":workSpaceName}, {"$push": {"Messages": {"from": getUserID(_from), "Message": Message, "time": getCurrentTime()[0],"date": getCurrentTime()[1], "msgType": "R", "ReadStatus": "True","type_":type_,"fileurl":MessageData['fileurl']}}})
        elif _from == toUser:
            Messages.update_one({"User": _from,"workSpaceName":workSpaceName}, {"$push": {toUser: {"Message": Message, "time": getCurrentTime()[0] ,"date": getCurrentTime()[1], "msgType": "S", "ReadStatus": "True","type_":type_,"fileurl":MessageData['fileurl']}}})
        else:
            Messages.update_one({"User": _from,"workSpaceName":workSpaceName}, {"$push": {toUser: {
                                "Message": Message, "time": getCurrentTime()[0] ,"date": getCurrentTime()[1], "msgType": "S", "ReadStatus": "True","type_":type_,"fileurl":MessageData['fileurl']}}})
            Messages.update_one({"User": toUser,"workSpaceName":workSpaceName}, {"$push": {_from: {
                                "Message": Message, "time": getCurrentTime()[0] ,"date": getCurrentTime()[1], "msgType": "R", "ReadStatus": "True","type_":type_,"fileurl":MessageData['fileurl']}}})    