from flask import Flask
import pymongo 

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os

# init app
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# setup MongoDB
connection_string = "mongodb+srv://msardidodev:n2EYar36WsPydAnA@todoapp.xcboila.mongodb.net/TodoApp?retryWrites=true&w=majority"

client = pymongo.MongoClient(connection_string, serverSelectionTimeoutMS=5000)
db = client.db

from src import routes