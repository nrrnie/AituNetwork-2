from flask import send_file
from aituNetwork.utils import utils
from utils import picturesDB


@utils.route('/get-picture/<filename>', methods=['GET'])
def get_picture(filename: str):
    path = picturesDB.get_picture_path('profile-pictures', filename)
    return send_file(path, mimetype='image/gif')
