from flask import request, render_template, session
from flask import redirect, url_for, flash
from passlib.hash import sha256_crypt
from aituNetwork.users import users
from aituNetwork.models import Users, ProfilePictures, Friends, Posts, UsersChats, Chats, Cities, EduPrograms
from aituNetwork import db
from utils import picturesDB, auth_required


@users.route('/profile/<slug>', methods=['GET'])
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


@users.route('/friends')
@auth_required
def friends():
    friend_list = Friends.get_friend_list(session['user'].id)
    return render_template('friends.html', user=session['user'], friend_list=friend_list)


@users.route('/messages')
@auth_required
def messages():
    user = session['user']
    chats = UsersChats.get_user_chats(user.id)
    chats = [Chats.get(chat.chat_id) for chat in chats]

    return render_template('messages.html', user=user, chats=chats)


@users.route('/settings', methods=['GET', 'POST'])
@auth_required
def settings():
    user = session['user']
    edu_programs = EduPrograms.get_edu_programs()
    cities = Cities.get_cities()

    if request.method == 'GET':
        return render_template('settings.html', user=user, cities=cities, edu_programs=edu_programs)

    picture = request.files.get('profile-picture')
    if picture:
        picture_name = picturesDB.add_picture('profile-pictures', picture)
        profile_picture = ProfilePictures(user_id=user.id, name=picture_name)
        db.session.add(profile_picture)

    slug = request.form.get('slug')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    about_me = request.form.get('about-me')
    birthday = request.form.get('birthday', None)
    birthday = None if birthday == '' else birthday
    city = request.form.get('city')
    course = request.form.get('course')
    edu_program = request.form.get('edu-program')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')

    print(city)

    if password != '':
        if password != password_confirm:
            flash('Passwords does not match')
            return redirect(url_for('users.settings'))
        password = sha256_crypt.hash(password)
    else:
        password = user.password

    if Users.is_slug_taken(slug) and slug != user.slug:
        flash('Slug is already taken.', 'danger')
        return redirect(url_for('users.settings'))

    update_info = dict(slug=slug, first_name=first_name, last_name=last_name, about_me=about_me, birthday=birthday,
                       city=city, course=course, edu_program=edu_program, password=password)
    Users.update_user_info(user.id, update_info)

    session['user'] = Users.query.get(user.id)

    flash('Info was updated', 'success')
    return redirect(url_for('users.settings'))


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


@users.route('/find-friends')
@auth_required
def find_friends():
    user = session['user']

    users_list = Users.get_users_for_new_friends_list(user.id)
    search = request.values.get('search', '')

    if search != '':
        users_list = users_list.filter(
            Users.first_name.like('%' + search + '%') | Users.last_name.like('%' + search + '%') | (
                    Users.barcode == search))

    users_list = users_list.paginate(1, 10)

    return render_template('find-friends.html', user=user, users=users_list, search=search)
