from pymongo import MongoClient



client = MongoClient('mongodb://192.168.1.169:27017/')
db = client.MadhukaranDb
user = db['Users']
messages = db['Messages']
groupList = db['GroupList']
UserDetails = db['UserDetails']
