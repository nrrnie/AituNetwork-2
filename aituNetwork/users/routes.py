from flask import request, render_template, session
from flask import redirect, url_for, flash
import functools
from aituNetwork.users import users
from aituNetwork.models import Users
from utils import picturesDB


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


@users.route('/<slug>', methods=['GET'])
@auth_required
def profile(slug: str):
    user = Users.query.filter_by(slug=slug).first()

    if user is None:
        return 'user is not found'

    current_user = session['user']

    return render_template('profile.html', current_user=current_user, profile_user=user)


@users.route('/settings', methods=['GET', 'POST'])
@auth_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html', user=session['user'])

    picture = request.files.get('profile-picture')
    if picture:
        picture_name = picturesDB.add_picture('profile-image', picture)
        # save picture_name to database

    flash('Info was updated')
    return redirect(url_for('users.settings'))

