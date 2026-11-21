from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import atexit
import signal
import sys

load_dotenv()

login_manager = LoginManager()

db = SQLAlchemy()

mongo_url = os.getenv("mongo_url")
mongo_client = MongoClient(mongo_url)

def mongo_connection_shutdown():
    mongo_client.close()

atexit.register(mongo_connection_shutdown)

for sig in (signal.SIGINT, signal.SIGTERM):
    signal.signal(sig, lambda s, f: (mongo_connection_shutdown(), sys.exit(0)))