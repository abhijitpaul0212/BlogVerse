from flask_user import UserMixin
from project.extensions import db


class User(db.Document, UserMixin):
    
    # Active set to True to allow login of user
    name = "User"
    active = db.BooleanField(default=True)
    
    # User authentication information
    username = db.StringField(default="")
    password = db.StringField()
    
    # User Information
    first_name = db.StringField(default="")
    last_name = db.StringField(default="")
    
    email = db.StringField(default="")
    email_confirmed_at = db.DateTimeField()
    
    # Relationships  (Roles: user or user and Admin)
    roles = db.ListField(db.StringField(), default=["user"])

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": ["email"],
    }
