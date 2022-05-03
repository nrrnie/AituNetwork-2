from flask import request, render_template, session
from flask import redirect, url_for, flash
import functools
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures
from aituNetwork import db
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
    profile_user = Users.query.filter_by(slug=slug).first()

    if profile_user is None:
        return 'user is not found'

    user = session['user']
    profile_picture = ProfilePictures.query.filter_by(user_id=user.id).order_by(ProfilePictures.id.desc()).first()
    if profile_picture:
        user.profile_picture = profile_picture.name

    return render_template('profile.html', user=user, profile_user=profile_user)


@users.route('/settings', methods=['GET', 'POST'])
@auth_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html', user=session['user'])

    picture = request.files.get('profile-picture')
    if picture:
        picture_name = picturesDB.add_picture('profile-pictures', picture)
        profile_picture = ProfilePictures(user_id=session['user'].id,  name=picture_name)
        db.session.add(profile_picture)
        db.session.commit()

    flash('Info was updated')
    return redirect(url_for('users.settings'))

