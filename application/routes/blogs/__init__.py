from flask import Blueprint

bp = Blueprint('blogs', __name__)

from application.routes.blogs import routes
