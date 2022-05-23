from flask import render_template, session
from aituNetwork.models import Posts
from aituNetwork.main import main
from utils import auth_required


@main.route('/home', methods=['GET'])
@auth_required
def home():
    user = session['user']

    posts = Posts.get_feed(user.id)

    return render_template('home.html', user=user, posts=posts)
