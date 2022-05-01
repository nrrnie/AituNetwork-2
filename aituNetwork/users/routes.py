from flask import render_template, session

from aituNetwork.users import users
from aituNetwork.models import Users


@users.route('/<slug>')
def profile(slug: str):
    user = Users.query.filter_by(slug=slug).first()

    if user is None:
        return 'user is not found'

    current_user = session['user']

    return render_template('profile.html', current_user=current_user, profile_user=user)
