from flask import Flask
from flask_cors import CORS
from .config import SECRET_KEY

# init app
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}}) # Allow any ports
# CORS(app, resources={r'/*': {'origins': 'http://localhost:8080', 'allow_headers': 'Access-Control-Allow-Origin'}}) # Allowing only the specified port


from src.controllers import todo