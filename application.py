import os
from flask_mongoengine import MongoEngineSessionInterface
from flask_user import UserManager
from flask import Flask
from config import DevelopmentConfig
from project.extensions import db
from project.routes.blogs import bp as blogs_bp
from project.routes.main import bp as main_bp
from project.models.user import User
from project.routes.blogs.routes import get_all_categories


if os.environ.get("FDT") == "ON":
    from flask_debugtoolbar import DebugToolbarExtension

application = Flask(__name__, static_folder="project//static", template_folder="project//templates")
app = application
app.config.from_object(__name__ + ".DevelopmentConfig")

if os.environ.get("FDT") == "ON":
    app.debug = True

# Setup Flask-MongoEngine --> MongoEngine --> PyMongo --> MongoDB
db.init_app(app)

UserManager(app, db, User)

# Use Flask Sessions with Mongoengine
app.session_interface = MongoEngineSessionInterface(db)

# Initiate the Flask Debug Toolbar Extension
if os.environ.get("FDT") == "ON":
    toolbar = DebugToolbarExtension(app)

# Register blueprints here
app.register_blueprint(blogs_bp)
app.register_blueprint(main_bp)

with app.app_context():
    get_all_categories()


if __name__ == '__main__':
    app.run()
