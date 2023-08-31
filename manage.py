import os
import datetime
from flask import Flask
import click
from flask.cli import with_appcontext

from project.extensions import db
from project.models.user import UserModel
from project.models.blog import CategoryMaster


basedir = os.path.abspath(os.path.dirname(__file__))

manage_app = Flask(__name__)
manage_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance/app.db')
db.init_app(manage_app)


@click.command(name='create_all_tables')
@with_appcontext
def create_all_tables():
    """Creates the db tables."""
    db.create_all()
    
@click.command(name='drop_all_tables')
@with_appcontext
def drop_all_tables():
    """Drops the db tables."""
    db.drop_all()

@click.command(name='create_admin')
@with_appcontext
def create_admin():
    """Creates the admin user."""
    admin_user = UserModel(
        email="ad@min.com",
        username='admin',
        password="admin",
        admin=True,
        confirmed=True,
        confirmed_on=datetime.datetime.now())
    db.session.add(admin_user)
    db.session.commit()
    print("Admin user created successfully", UserModel.query.filter_by(email='ad@min.com').first().email)
    
@click.command(name='create_new_category')
@click.argument('category_name')
@with_appcontext
def create_new_category(category_name):
    category = CategoryMaster(
        category_name=category_name
    )
    db.session.add(category)
    db.session.commit()
    print("Category added successfully", CategoryMaster.query.filter_by(category_name=category_name).first().category_name)

    
# add command function to cli commands
manage_app.cli.add_command(create_all_tables)
manage_app.cli.add_command(drop_all_tables)
manage_app.cli.add_command(create_admin)
manage_app.cli.add_command(create_new_category)