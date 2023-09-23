import os
from flask_mongoengine import MongoEngineSessionInterface
from flask_user import UserManager
from flask import Flask
from config import DevelopmentConfig
from application.extensions import db
from application.routes.blogs import bp as blogs_bp
from application.routes.main import bp as main_bp
from application.models.user import User
from application.routes.blogs.routes import get_all_categories


if os.environ.get("FDT") == "ON":
    from flask_debugtoolbar import DebugToolbarExtension


# --- // Application Factory Setup (based on the Flask-User example for MongoDB)
# https://flask-user.readthedocs.io/en/latest/mongodb_app.html
def create_app():    
    # Setup Flask and load app.config
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(__name__ + ".DevelopmentConfig")
    # csrf = CSRFProtect(app)
    # csrf.init_app(app)

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

    return app
