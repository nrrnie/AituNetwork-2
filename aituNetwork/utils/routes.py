from flask import request, send_file, render_template
from aituNetwork.models import PostLikes, Users
from aituNetwork.utils import utils
from utils import picturesDB


@utils.route('/get-picture/<filename>', methods=['GET'])
def get_picture(filename: str):
    path = picturesDB.get_picture_path('profile-pictures', filename)
    return send_file(path, mimetype='image/gif')


@utils.route('/like', methods=['POST'])
def like():
    post_id = int(request.form.get('post-id'))
    user_id = int(request.form.get('user-id'))

    PostLikes.add(user_id, post_id)

    return dict(status='ok')


@utils.route('/unlike', methods=['POST'])
def unlike():
    post_id = int(request.form.get('post-id'))
    user_id = int(request.form.get('user-id'))

    PostLikes.remove(user_id, post_id)

    return dict(status='ok')


@utils.route('/generate-message', methods=['POST'])
def generate_message():
    user_id = int(request.form.get('user_id'))
    message = request.form.get('message')

    return render_template('message.html', user=Users.get(user_id), message=message)
