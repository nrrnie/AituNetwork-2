from flask import Blueprint

utils = Blueprint('utils', __name__)

from aituNetwork.utils import routes
