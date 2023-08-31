from flask import Blueprint

bp = Blueprint('blogs', __name__)

from project.routes.blogs import routes