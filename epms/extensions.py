from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

login_manager = LoginManager()

db = SQLAlchemy()

mongo_url = os.getenv("mongo_url")
mongo_cluster = MongoClient(mongo_url)

