# This file maintains all project level configurations
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    """Base configuration"""
    SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = False
    DEBUG_TB_ENABLED = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'
    
    # mail settings
    MAIL_SERVER = os.environ.get('APP_MAIL_SERVER', 'smtp.googlemail.com')
    MAIL_PORT = int(os.environ.get('APP_MAIL_PORT', 465))
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']

    # mail accounts
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Flask-MongoEngine settings
    MONGO_DB_URL = os.environ.get('MONGO_DB_URL')
    MONGODB_SETTINGS = {
        'host': MONGO_DB_URL,
        'db': 'MyBlogs',
        'tlscafile': certifi.where()
    }
    
    # Shown in email templates and page footers
    USER_APP_NAME = "BlogVerse"
    USER_ENABLE_EMAIL = True                    # Enable email authentication
    USER_ENABLE_USERNAME = True                 # Enable username authentication
    USER_ENABLE_CONFIRM_EMAIL = True            # Enable email after registration
    USER_ENABLE_FORGOT_PASSWORD = True          # Enable email after forgot password
    USER_ENABLE_CHANGE_PASSWORD = True          # Enable email after password change
    USER_SEND_PASSWORD_CHANGED_EMAIL = True     # Enable email after password change
    USER_REQUIRE_RETYPE_PASSWORD = True
    USER_ENABLE_CHANGE_USERNAME = False
    
    # Flask User Manager Configuration
    USER_COPYRIGHT_YEAR = 2023
    USER_CORPORATION_NAME = "AbhijitPaul"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    DEBUG_TB_ENABLED = True
