print ("Loadded.")
from pymongo import MongoClient
connect = "DBURL"
global client
client = MongoClient(connect)
def get_database():
    return client['servers']
def get_served():
    return client['served']