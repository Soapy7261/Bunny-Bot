print ("Loadded.")
from pymongo import MongoClient
connect = "DBURL"
global client
client = MongoClient(connect)
def get_database():
    return client['betaservers']
def get_served():
    return client['betaserved']
#Looking back at this, this was never used since i disabled the commands that used it lol.