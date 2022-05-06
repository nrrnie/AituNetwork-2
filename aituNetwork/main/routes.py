from flask import render_template, session
from aituNetwork.main import main
from utils import auth_required


@main.route('/home', methods=['GET'])
@auth_required
def home():
    user = session['user']
    return render_template('home.html', user=user)
