from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import unique
from project.extensions import db , login_manager
import datetime


class User(db.Document, UserMixin):
    
    # Active set to True to allow login of user
    name = "User"
    active = db.BooleanField(default=True)
    
    # User authentication information
    email = db.StringField(default="")
    username = db.StringField(default="")
    password = db.StringField()
    registered_on = db.DateTimeField()
    admin = db.BooleanField(default=True)
    confirmed = db.BooleanField(default=True)
    confirmed_on = db.DateTimeField()
    
    # Relationships  (Roles: user or user and Admin)
    roles = db.ListField(db.StringField(), default=["user"])

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": ["email"],
    }    
    
    # def set_password(self, password):
    #     return generate_password_hash(password)
        
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
    
    # def check_confirmed(self):
    #     return self.confirmed
    
    # def set_confirmed(self, confirmed=True):
    #     self.confirmed = confirmed

    def get_id(self):
        return self.name


# @login_manager.user_loader
# def load_user(user_id):
#     user = User.objects(name=user_id)[0]
#     return user

