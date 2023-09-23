from flask import Blueprint

bp = Blueprint('main', __name__)

from application.routes.main import routes