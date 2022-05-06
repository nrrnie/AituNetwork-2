from flask import request, render_template, session
from flask import redirect, url_for, flash
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures
from aituNetwork import db
from utils import picturesDB, auth_required


@users.route('/<slug>', methods=['GET'])
@auth_required
def profile(slug: str):
    profile_user = Users.query.filter_by(slug=slug).first()

    if profile_user is None:
        return 'user is not found'

    profile_picture = ProfilePictures.query.filter_by(user_id=profile_user.id).order_by(ProfilePictures.id.desc()).first()
    if profile_picture:
        profile_user.profile_picture = profile_picture.name

    user = session['user']

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

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


@users.route('/friends', methods=['GET'])
@auth_required
def friends():
    if request.method == 'GET':
        return render_template('friends.html', user=session['user'])
