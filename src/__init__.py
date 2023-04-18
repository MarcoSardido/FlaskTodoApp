from flask import Flask
# import certifi

# from pymongo import MongoClient

import os
from dotenv import load_dotenv, find_dotenv

# init app
app = Flask(__name__)

load_dotenv(find_dotenv())

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# setup MongoDB

# MongoDB Atlas URI
# connection = os.environ.get('MONGO_URI')

# Docker URI
# connection = os.environ.get('MONGO_DOCKER_URI')

# Create a new client and connect to the server
# client = MongoClient(connection)

# Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print('Error at pinging mongodb', e)


# Database and Collections
# myDB = client['todo_data']
# todoCollection = myDB['todos']


from src.controllers import todo