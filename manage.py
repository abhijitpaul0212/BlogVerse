import os
import datetime
from flask import Flask
import click
from flask.cli import with_appcontext
from flask_mongoengine import MongoEngineSessionInterface
from src.extensions import db
from src.models.blog import Category
from config import DevelopmentConfig


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object(__name__ + ".DevelopmentConfig")
db.init_app(app)

# Use Flask Sessions with Mongoengine
app.session_interface = MongoEngineSessionInterface(db)
   
@click.command()
@click.option('--name', help='Name of category')
def create_category(name):
    category = Category(
        category_name=name
    )
    category.save()
    print("Category '{}' added successfully".format(Category.objects(category_name=name).first().category_name))

    
if __name__ == '__main__':
    create_category()