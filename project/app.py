import os

import json

import datetime

from flask_mongoengine import (
    MongoEngine,
    MongoEngineSessionInterface,
)

from flask_user import (
    login_required,
    UserManager,
    UserMixin,
    current_user,
    roles_required,
)

from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)

from config import DevelopmentConfig


if os.environ.get("FDT") == "ON":
    from flask_debugtoolbar import DebugToolbarExtension

# --- // Application Factory Setup (based on the Flask-User example for MongoDB)
# https://flask-user.readthedocs.io/en/latest/mongodb_app.html
# Setup Flask and load app.config
app = Flask(__name__, static_folder="static", template_folder="templates")
app.config.from_object(__name__ + ".DevelopmentConfig")
# csrf = CSRFProtect(app)
# csrf.init_app(app)

if os.environ.get("FDT") == "ON":
    app.debug = True

# Setup Flask-MongoEngine --> MongoEngine --> PyMongo --> MongoDB
db = MongoEngine(app)

# Use Flask Sessions with Mongoengine
app.session_interface = MongoEngineSessionInterface(db)

# Initiate the Flask Debug Toolbar Extension
if os.environ.get("FDT") == "ON":
    toolbar = DebugToolbarExtension(app)


# --- // Classes -> MongoDB Collections: User, Venue, Review
# Flask-User User Class (Collection) extended with email_confirmed_at
# Added username indexing and background-indexing for performance
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


# Setup Flask-User and specify the User data-model
user_manager = UserManager(app, db, User)


def password_hashing(password):
    return user_manager.hash_password(password)
    

# --- // BlogVerse Main Routes (Endpoints): CRUD.
@app.route("/")
@app.route("/index")
@app.route("/index.htm")
@app.route("/index.html")
def home_page():
    """
    Landing/Home Page, accessible before sign in/login. If logged in, user is redirected to the Main Page.
    At first access/touch the user 'admin' is created using environment variables for the password and email address.
    The admin user creation is here as it will be created twice on Heroku if placed in the main code.
    """

    # Create admin user as first/default user, if admin does not exist.
    # Password and e-mail are set using environment variables.
    all_users = [all_user.username for all_user in User.objects.all()]

    if 'admin' not in all_users:
        try:
            user = User(
                username="admin",
                first_name="Administrator",
                last_name="Administrator",
                email='ad@min.com',
                email_confirmed_at=datetime.datetime.utcnow(),
                password=password_hashing('admin'),
            )
            user.roles.append("Admin")
            user.save()

            flash("'admin' account created.", "success")
            app.logger.info(
                "'admin' account is created at startup if the user doesn't exist: [SUCCESS] - (index.html)."
            )
        except Exception:
            flash("'admin' account not created.", "danger")
            app.logger.critical(
                "'admin' account is created at startup if the user doesn't exist: [FAILURE] - (index.html)."
            )
    return redirect(url_for('list_all_blogs'))


# Global variable
global_all_category_num = []
global_all_category_name = []


def get_all_categories():
    global global_all_category_num, global_all_category_name

    for cat in Category.objects.all():
        dict_cat = json.loads(cat.to_json())
        global_all_category_num.append(dict_cat['_id']['$oid'])
        global_all_category_name.append(dict_cat['category_name'])


@app.route("/blogs")
def blogs():
    return redirect(url_for('list_all_blogs'))

# CRUD for Blogs


@app.route("/listAllBlogs")
def list_all_blogs():
    all_blogs = Blog.objects.all()
    all_blogs = [all_blog for all_blog in all_blogs]
    all_users = User.objects.all()
    all_users = [all_user for all_user in all_users]
    all_categories = Category.objects.all()
    all_categories = [all_cat for all_cat in all_categories]
    return render_template('blogs/list_all_blogs.html', all_blogs=all_blogs, all_users=all_users, all_categories=all_categories)


@app.route("/createBlog", methods=['GET', 'POST'])
@login_required
def create_blog():
    if request.method == 'POST':
        category_id = request.form.get("category_id")
        blog_text = request.form.get("blog_text")
        today = datetime.datetime.utcnow()
        blog_user_id = current_user.id
        blog_read_count = 0
        blog_rating_count = 0

        newBlog = Blog(category_id=category_id,
                       blog_user_id=blog_user_id,
                       blog_text=blog_text,
                       blog_creation_date=today,
                       blog_read_count=blog_read_count,
                       blog_rating_count=blog_rating_count)

        newBlog.save()
        return redirect("blogs")
    else:
        return render_template("blogs/create_blog.html", all_category_id=global_all_category_num, all_category_name=global_all_category_name)


@app.route("/viewBlog")
@login_required
def view_blogs():
    all_categories = Category.objects.all()
    all_categories = [all_cat for all_cat in all_categories]

    user = User.objects.filter(id=current_user.id).all()[0]

    if user.username == 'admin':
        all_self_blogs = Blog.objects.all()
    else:
        all_self_blogs = Blog.objects.filter(blog_user_id=current_user.id).all()
    return render_template("blogs/view_blog.html", all_self_blogs=all_self_blogs, all_categories=all_categories)


@app.route("/self_blog_detail/<string:blog_id>/<string:blog_category>", methods=["GET", "POST"])
@login_required
def self_blog_detail(blog_id, blog_category):
    blog = Blog.objects.filter(id=blog_id).first()
    if request.method == "POST":
        if request.form['action'] == 'Update':
            blog.blog_text = request.form.get('blog_text')
        elif request.form['action'] == 'Delete':
            Blog.objects.filter(id=blog_id).first().delete()
        blog.save()
        return redirect('/viewBlog')
    return render_template("blogs/self_blog_detail.html", blog_text=blog.blog_text)


@app.route('/blogDetail/<string:blog_id>/<string:username>/<string:blog_category>', methods=["GET", "POST"])
@login_required
def blog_detail(blog_id, username, blog_category):
    blog = Blog.objects.filter(id=blog_id).first()
    if request.method == 'GET':
        if current_user.id != blog.blog_user_id:
            blog.blog_read_count += 1
            blog.save()

        blog_rating = None
        avg_ratings = list(Comment.objects.aggregate([{'$group': {'_id': '$blog_id', 'avgRating': {'$avg': '$blog_rating'}}}]))
        for rating in avg_ratings:
            if str(list(rating.values())[0]) == blog_id:
                blog_rating = list(rating.values())[1]

        return render_template('blogs/blog_detail.html', blog=blog, rating=blog_rating, author=username, category=blog_category)
    else:
        rate = request.form.get('rating')
        comment = request.form.get('comment')
        blog_id = request.form.get('blog_id')

        old_comment = Comment.objects.filter(blog_id=blog_id).filter(comment_user_id=current_user.id).first()
        today = datetime.datetime.utcnow()

        if old_comment is None:
            blog.blog_rating_count += 1
            blog.save()

            new_comment = Comment(
                blog_id=blog_id,
                comment_user_id=current_user.id,
                blog_comment=comment,
                blog_rating=rate,
                blog_comment_date=today)
            new_comment.save()
        else:
            old_comment.blog_comment = comment
            old_comment.blog_rating = rate
            old_comment.save()
        return redirect('/blogs')


with app.app_context():
    get_all_categories()


# --- // Error Handlers for 404 Page Not Found, 405 Method Not Allowed, and 500 Internal Server Error.

@app.errorhandler(404)
def not_found(error):
    excuse = "Apologies, our Staff are lost in the Safe Havens! Please click on [ Home ] to go to the Home Page, or click on [ Sign Out ] below."
    return render_template("oops.html", error=error, excuse=excuse, error_type="Client: 404 - Page Not Found")


@app.errorhandler(405)
def not_allowed(error):
    excuse = "Apologies, our Staff won't allow you to do this! Please click on [ Home ] to go to the Home Page, or click on [ Sign Out ] below."
    return render_template("oops.html", error=error, excuse=excuse, error_type="Client: 405 - Method Not Allowed")


@app.errorhandler(500)
def internal_error(error):
    excuse = "Apologies, something serious occurred and the Staff are working on resolving the issue! This section is cordoned off for now. Please click on [ Home ] to go to the Home Page, or click on [ Sign Out ] below."
    return render_template("oops.html", error=error, excuse=excuse, error_type="Server: 500 - Internal Server Error")


if __name__ == "__main__":
    if os.environ.get("APPDEBUG") == "ON":
        app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=True)
    else:
        app.run(host=os.environ.get("IP"), port=os.environ.get("PORT"), debug=False)
