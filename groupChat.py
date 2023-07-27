from pymongo import MongoClient
# Directory Import Files
from chatlib import *
from Database.databaseConfig import *


# # Database connection
# client = MongoClient('mongodb://192.168.1.221:27017/')
# db = client.MadhukaranDb
# user = db['Users']
# messages = db['Messages']
# groupList = db['GroupList']


def getTotalGroupList():
    return [temp['groupName'] for temp in GroupList.find({}, {"_id": 0, "groupName": 1})]




