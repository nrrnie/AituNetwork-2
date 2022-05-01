from flask import render_template
from aituNetwork.main import main


@main.route('/home', methods=['GET'])
def home():
    return render_template('home.html')
