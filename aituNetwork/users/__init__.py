from flask import Blueprint

users = Blueprint('users', __name__, template_folder='templates', static_folder='static')

from aituNetwork.users import routes
from aituNetwork.users import template_functions

