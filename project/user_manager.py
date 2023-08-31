from flask_user import UserManager
from project import app
from project.models.user import UserModel
from project.extensions import db

# User Manager
# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, UserModel)
