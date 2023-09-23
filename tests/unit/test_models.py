from project.models.user import User
from project.models.blog import Blog, Comment
from werkzeug.security import generate_password_hash
import datetime
import json
import logging
from bson import ObjectId

LOGGER = logging.getLogger(__name__)


def test_add_user(client):
    """This unit test verifies the functionality of adding new user
    """
    user = User(
                username="test_user",
                first_name="test_user",
                last_name="",
                email='test_user@gmail.com',
                email_confirmed_at=datetime.datetime.utcnow(),
                password=generate_password_hash('test@123'),
            )
    user.save()

    assert user.email == "test_user@gmail.com"
    assert user.password != 'test@123'
    assert user.first_name == "test_user"
    
    # user.delete()
    # assert user.email not in [all_user.email for all_user in
    #                           User.objects.all()]


def test_add_blog(client, globals):
    """This unit test verifies the functionality of adding new blog
    """
    user_id = None
    for user in User.objects.all():
        if user.username == 'test_user':
            user_id = json.loads(user.to_json())['_id']['$oid']

    newBlog = Blog(category_id=globals[1][globals[0].index('Python')],
                   blog_user_id=user_id,
                   blog_text="New Python blog",
                   blog_creation_date=datetime.datetime.utcnow(),
                   blog_read_count=0,
                   blog_rating_count=0)

    newBlog.save()
    assert "New Python blog" in [all_blog.blog_text for all_blog in
                                 Blog.objects.all()]


def test_add_comment(client):
    """This unit test verifies the functionality of adding new blog
    """
    user_id, blog_id = None, None
    for user in User.objects.all():
        if user.username == 'test_user':
            user_id = json.loads(user.to_json())['_id']['$oid']
    
    for blog in Blog.objects.all():
        if blog.blog_user_id == ObjectId(user_id) and "New Python blog" in blog.blog_text:
            blog_id = json.loads(blog.to_json())['_id']['$oid']
    
    newComment = Comment(blog_id=blog_id,
                         blog_comment="Nicely written Python blog",
                         comment_user_id=user_id,
                         blog_rating="5",
                         blog_comment_date=datetime.datetime.utcnow())

    newComment.save()
    assert "Nicely written Python blog" in [comment.blog_comment for comment in
                                            Comment.objects.all()]


def test_delete_comment(client):
    user_id, blog_id, comment_id = None, None, None
    for user in User.objects.all():
        if user.username == 'test_user':
            user_id = json.loads(user.to_json())['_id']['$oid']
    
    for blog in Blog.objects.all():
        if blog.blog_user_id == ObjectId(user_id) and "New Python blog" in blog.blog_text:
            blog_id = json.loads(blog.to_json())['_id']['$oid']
    
    for comment in Comment.objects.all():
        if comment.blog_id == ObjectId(blog_id):
            comment_id = json.loads(comment.to_json())['_id']['$oid']
    
    assert "Nicely written Python blog" in [all_comment.blog_comment for all_comment in Comment.objects.all()]
    
    Comment.objects.filter(id=comment_id).first().delete()
    
    assert "Nicely written Python blog" not in [all_comment.blog_comment for all_comment in Comment.objects.all()]


def test_delete_blog(client):
    user_id, blog_id = None, None
    for user in User.objects.all():
        if user.username == 'test_user':
            user_id = json.loads(user.to_json())['_id']['$oid']
    
    for blog in Blog.objects.all():
        if blog.blog_user_id == ObjectId(user_id) and "New Python blog" in blog.blog_text:
            blog_id = json.loads(blog.to_json())['_id']['$oid']
    
    assert "New Python blog" in [all_blog.blog_text for all_blog in
                                 Blog.objects.all()]
    
    Blog.objects.filter(id=blog_id).first().delete()
    
    assert "New Python blog" not in [all_blog.blog_text for all_blog in
                                     Blog.objects.all()]


def test_delete_user(client):
    user_id = None
    for user in User.objects.all():
        if user.username == 'test_user':
            user_id = json.loads(user.to_json())['_id']['$oid']
    
    assert "test_user" in [all_user.username for all_user in User.objects.all()]

    User.objects.filter(id=user_id).first().delete()

    assert "test_user" not in [all_user.username for all_user in User.objects.all()]
