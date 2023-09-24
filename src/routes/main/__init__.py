from flask import Blueprint

bp = Blueprint('main', __name__)

from src.routes.main import routes