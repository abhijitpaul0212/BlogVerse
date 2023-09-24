from flask import Blueprint

bp = Blueprint('blogs', __name__)

from src.routes.blogs import routes
