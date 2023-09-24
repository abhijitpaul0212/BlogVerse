from src.extensions import db
from src.models.user import User


class Category(db.Document):
    category_name = db.StringField(default="")

    meta = {
        "auto_create_index": True,
        "index_background": True
    }


class Blog(db.Document):
    category_id = db.ObjectIdField(Category)
    blog_user_id = db.ObjectIdField(User)
    blog_text = db.StringField(default="")
    blog_creation_date = db.DateTimeField()
    blog_read_count = db.IntField(default=0)
    blog_rating_count = db.IntField(default=0)

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": ["category_id", "blog_user_id"]
    }


class Comment(db.Document):
    blog_id = db.ObjectIdField(Blog)
    blog_comment = db.StringField(default="")
    comment_user_id = db.ObjectIdField(User)
    blog_rating = db.IntField()
    blog_comment_date = db.DateTimeField()

    meta = {
        "auto_create_index": True,
        "index_background": True,
        "indexes": ["blog_id"]
    }
