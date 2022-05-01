from flask import render_template, request, flash
from passlib.hash import sha256_crypt
from aituNetwork.auth import auth

from aituNetwork.models import Users


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    barcode = request.form.get('barcode')
    password = request.form.get('password')

    user = Users.query.filter_by(barcode=barcode).first()

    if user is not None and sha256_crypt.verify(password, user.password):
        return 'main page'

    flash('Barcode or password is wrong')

    return render_template('login.html')


@auth.route('/register', methods=['GET'])
def register():
    return render_template('register.html')
