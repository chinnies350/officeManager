"""
This is the basic Database Configuration files for the database connection for the ChatApplication.
# For Database connections Refer The Import File "databaseLib.py"
# For the Other Basic Related Functions Refer The Import File "chatlib.py"
"""

from pymongo import MongoClient



client = MongoClient('mongodb://192.168.1.169:27017/')
# client = MongoClient('mongodb://127.0.0.1:27017/')  
db = client.MadhukaranDb
Users = db['Users']
Messages = db['Messages']
GroupList = db['GroupList']
UserDetails = db['UserDetails']
EmailVerification = db['EmailVerification']
workSpace = db['workSpace']
session_token = db['session']
active_users = db['active_users']


# routes = web.RouteTableDef()
websockets = set()
history = []
test = {}