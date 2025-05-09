from dotenv import load_dotenv
import os

load_dotenv() 
#connect to mongoDB server
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
user_name = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
app_name = os.getenv("MONGODB_APPNAME")
cluster_name = os.getenv("MONGODB_CLUSTER")
uri = f"mongodb+srv://{user_name}:{password}@{cluster_name}.lzb32h6.mongodb.net/?retryWrites=true&w=majority&appName={app_name}"
# Create a new client and connect to the server
client = None
if(not client):
    client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    # client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
