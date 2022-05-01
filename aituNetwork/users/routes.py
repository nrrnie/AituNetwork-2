from flask import render_template

from aituNetwork.users import users


@users.route('/profile')
def profile():
    return render_template('profile.html', current_user={}, profile_user={})
