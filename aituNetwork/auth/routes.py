from flask import render_template, request, flash, session
from flask import redirect, url_for
from passlib.hash import sha256_crypt


from aituNetwork.auth import auth
from aituNetwork.models import Users
from aituNetwork import db


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    barcode = request.form.get('barcode')
    password = request.form.get('password')

    user = Users.query.filter_by(barcode=barcode).first()

    if user is not None and sha256_crypt.verify(password, user.password):
        session['user'] = user
        return redirect(url_for('main.home'))

    flash('Barcode or password is wrong')

    return render_template('login.html')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    barcode = request.form.get('barcode')
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    password = request.form.get('password')
    password_confirm = request.form.get('password-confirm')

    if password == password_confirm:
        user = Users.query.filter_by(barcode=barcode).first()
        if user is None:
            hashed_password = sha256_crypt.hash(password)
            user = Users(barcode=barcode, first_name=first_name, last_name=last_name, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            flash('User was successfully created!')
            return redirect(url_for('auth.login'))
        else:
            flash('Barcode is already registered')
    else:
        flash('Passwords does not match')

    return render_template('register.html')


@auth.route('/logout', methods=['GET'])
def logout():
    return ''
