from flask import request, render_template, session
from flask import redirect, url_for, flash
from passlib.hash import sha256_crypt
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

    posts = Posts.get_posts(profile_user.id)

    user = session['user']

    friend_status = Friends.get_friend_status(user.id, profile_user.id)
    friend_list = Friends.get_friend_list(profile_user.id)[:6]

    return render_template('profile.html', user=user, profile_user=profile_user, friend_status=friend_status,
                           posts=posts, friend_list=friend_list)


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
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')

    if password != password_confirm:
        flash('Passwords does not match')
        return redirect(url_for('users.settings'))

    if Users.is_slug_taken(slug) and slug != session['user'].slug:
        flash('Slug is already taken.', 'danger')
        return redirect(url_for('users.settings'))

    update_info = dict(slug=slug, first_name=first_name, last_name=last_name, about_me=about_me,
                       password=sha256_crypt.hash(password))
    Users.update_user_info(session['user'].id, update_info)

    session['user'] = Users.query.get(session['user'].id)

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


@users.route('/friends')
@auth_required
def friends():
    friend_list = Friends.get_friend_list(session['user'].id)
    return render_template('friends.html', user=session['user'], friend_list=friend_list)


@users.route('/add/friend')
@auth_required
def add_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    Friends.add_friend(user_id, friend_id)

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))


@users.route('/remove/friend')
@auth_required
def remove_friend():
    user_id = request.values.get('user_id')
    friend_id = request.values.get('friend_id')

    Friends.remove_friend(user_id, friend_id)

    return redirect(url_for('users.profile', slug=Users.query.get(friend_id).slug))


@users.route('/add/post', methods=['POST'])
@auth_required
def add_post():
    post_content = request.form.get('post-content')

    Posts.add_post(session['user'].id, post_content)

    flash('Your post is added!', 'success')
    return redirect(url_for('users.profile', slug=session['user'].slug))
