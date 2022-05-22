from flask import request, render_template, session
from flask import redirect, url_for, flash
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures, Friends, Posts
from aituNetwork import db
from utils import picturesDB, auth_required


@users.route('/<slug>', methods=['GET'])
@auth_required
def profile(slug: str):
    profile_user = Users.query.filter_by(slug=slug).first()

    if profile_user is None:
        return 'user is not found'

    profile_picture = ProfilePictures.get_profile_picture(profile_user.id)
    if profile_picture:
        profile_user.profile_picture = profile_picture.name

    posts = Posts.query.filter_by(user_id=profile_user.id).order_by(Posts.id.desc()).all()

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

    return render_template('profile.html', user=user, profile_user=profile_user, friend_status=friend_status,
                           posts=posts)


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

    slug = request.form.get('slug')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    about_me = request.form.get('about-me')

    if Users.query.filter_by(slug=slug).first() is not None and slug != session['user'].slug:
        flash('Slug is already taken.', 'danger')
        return redirect(url_for('users.settings'))

    Users.query.filter_by(id=session['user'].id).update(
        dict(slug=slug, first_name=first_name, last_name=last_name, about_me=about_me))
    db.session.commit()

    session['user'] = Users.query.get(session['user'].id)

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


@users.route('/friends', methods=['GET'])
@auth_required
def friends():
    if request.method == 'GET':
        return render_template('friends.html', user=session['user'])


@users.route('/add/friend')
@auth_required
def add_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is None:
        friend = Friends(user_id=user_id, friend_id=friend_id)
        db.session.add(friend)
        db.session.commit()

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))


@users.route('/remove/friend')
@auth_required
def remove_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    if Friends.query.filter_by(user_id=user_id, friend_id=friend_id).first() is not None:
        Friends.query.filter_by(user_id=user_id, friend_id=friend_id).delete()
        db.session.commit()

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))


@users.route('/add/post', methods=['POST'])
@auth_required
def add_post():
    post_content = request.form.get('post-content')

    post = Posts(user_id=session['user'].id, content=post_content)
    db.session.add(post)
    db.session.commit()

    flash('Your post is added!', 'success')
    return redirect(url_for('users.profile', slug=session['user'].slug))
