from flask import render_template
from aituNetwork.auth import auth


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')
