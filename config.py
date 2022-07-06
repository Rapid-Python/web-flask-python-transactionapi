from flask import Flask
import os
from flask_pymongo import PyMongo
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config['HOST'] = os.getenv('HOST')
app.config['PORT'] = os.getenv('PORT')
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
app.config['COLLECTION'] = 'blockchain'
mongodb_client = PyMongo(app)
db = mongodb_client.db
mycollection = db[app.config['COLLECTION']]
