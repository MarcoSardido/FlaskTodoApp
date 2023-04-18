import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

SECRET_KEY = os.environ.get('SECRET_KEY') # For CSRF
MONGO_DOCKER_URI = os.environ.get('MONGO_DOCKER_URI') # Mongodb Docker
MONGO_URI = os.environ.get('MONGO_URI') # Mongodb Atlas

# Todo Model
HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')
