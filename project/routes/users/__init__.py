from flask import Blueprint

bp = Blueprint('users', __name__)

from project.routes.users import routes