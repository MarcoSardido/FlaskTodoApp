from flask import Flask
import certifi

from pymongo import MongoClient

import os
from dotenv import load_dotenv, find_dotenv

# init app
app = Flask(__name__)

load_dotenv(find_dotenv())

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# setup MongoDB
connection = os.environ.get('MONGO_URI')
# connection = os.environ.get('MONGO_CONTAINER_URI')

# Create a new client and connect to the server
client = MongoClient(connection, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

myDB = client['todo_data']
todoCollection = myDB['todos']


from src import routes