from pymongo import MongoClient
from flask_login import LoginManager
from flask_mail import Mail
import certifi
from flask_mongoengine import (
    MongoEngine,
    MongoEngineSession,
    MongoEngineSessionInterface,
)

# Create a ORM
# MONGODB_URI = "mongodb+srv://root:root@cluster0.k3s4vuf.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
# client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
# db = client.myblogs

# Setup Flask-MongoEngine --> MongoEngine --> PyMongo --> MongoDB

MONGO_DB_URL = "mongodb+srv://root:root@cluster0.k3s4vuf.mongodb.net?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
MONGODB_SETTINGS = {
        "db": "myblogs",
        "host": MONGO_DB_URL,
        'connect': False,
        "alias": "myblogs",
    }
db = MongoEngine(config=MONGODB_SETTINGS)
session_interface = MongoEngineSessionInterface(db)
print(db)


# Login Manager
login_manager = LoginManager()

# Mail
mail = Mail()
