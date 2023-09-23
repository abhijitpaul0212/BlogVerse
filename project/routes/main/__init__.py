from flask import Blueprint

bp = Blueprint('main', __name__)

from project.routes.main import routes