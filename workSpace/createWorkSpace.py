from Database.databaseConfig import *
from Database.databaseConfig import workSpace, Users

from common.commonFunctions import *



# Get UserID for Username
def getUserID(userName):
    return Users.find_one({"username": userName}, {"_id": 0, "userId": 1})['userId']



def getUserListForWorkspace(workSpaceName):
    try:
        from common.commonFunctions import getUserName
        return [getUserName(temp).replace(" ","_") for temp in workSpace.find_one({"workSpaceName":workSpaceName},{"_id":0,"users":1})['users']]
    except:
        return []

# def getGroupListForWorkspace(workSpaceName):
#     try:
#         return workSpace.find_one({"workSpaceName":workSpaceName},{"_id":0,"GroupList":1})['GroupList']
#     except:
#         return "wrong with getting grouplist"


def new_getGroupListForWorkspace(username,workSpaceName):
    try:
        g = []
        groups_ = workSpace.find_one({"workSpaceName":workSpaceName},{"_id":0,"GroupList":1})['GroupList']
        for group in groups_:
            userlist = [getUserName(temp) for temp in GroupList.find_one({"workSpaceName":workSpaceName,"groupName":group},{"_id":0,"Users":1})['Users']]
            if username in userlist:
                g.append(group)
        return g
    except:
        return "wrong with getting grouplist"


def createWorkspace(workSpaceName,userName,description):
    userName = getUserID(userName)
    workSpace.insert({"workSpaceName":workSpaceName,"admin":userName,"users":[userName],"GroupList":[]})
