from flask import request, render_template, session
from flask import redirect, url_for, flash
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures, Friends
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

    is_my_friend = Friends.query.filter_by(user_id=user.id, friend_id=profile_user.id).first()
    am_i_friend = Friends.query.filter_by(user_id=profile_user.id, friend_id=user.id).first()

    # friend_status
    # 1: I sent request
    # 2: Profile user sent request
    # 3: Friends

    friend_status = None
    if is_my_friend is not None and am_i_friend is not None:
        friend_status = 3
    elif is_my_friend is not None:
        friend_status = 1
    elif am_i_friend is not None:
        friend_status = 2

    return render_template('profile.html', user=user, profile_user=profile_user, friend_status=friend_status)


@users.route('/settings', methods=['GET', 'POST'])
@auth_required
def settings():
    if request.method == 'GET':
        return render_template('settings.html', user=session['user'])

    picture = request.files.get('profile-picture')
    if picture:
        picture_name = picturesDB.add_picture('profile-pictures', picture)
        profile_picture = ProfilePictures(user_id=session['user'].id, name=picture_name)
        db.session.add(profile_picture)
        db.session.commit()

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


@users.route('/add/friend')
@auth_required
def add_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')
    friend = Friends(user_id=user_id, friend_id=friend_id)
    db.session.add(friend)
    db.session.commit()
    return "Friend request is sent"
