from flask import Blueprint

utils = Blueprint('utils', __name__, template_folder='templates')

from aituNetwork.utils import routes
