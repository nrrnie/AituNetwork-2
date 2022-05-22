from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from flask import render_template, request, flash, session
from flask import redirect, url_for
from passlib.hash import sha256_crypt
from os import getenv
import functools

from aituNetwork.auth import auth
from aituNetwork.models import Users
from aituNetwork import db

from utils import send_email


url_serializer = URLSafeTimedSerializer(getenv('SECRET_KEY'))


def redirect_if_logged(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is not None:
            return redirect(url_for('users.profile', slug=session['user'].slug))
        return func(*args, **kwargs)
    return wrapper


@auth.route('/login', methods=['GET', 'POST'])
@redirect_if_logged
def login():
    if request.method == 'GET':
        return render_template('login.html')

    barcode = request.form.get('barcode')
    password = request.form.get('password')

    user = Users.query.filter_by(barcode=barcode).first()

    if user is not None and sha256_crypt.verify(password, user.password):
        session['user'] = user
        return redirect(url_for('main.home'))

    flash('Barcode or password is wrong', 'danger')

    return redirect(url_for('auth.login'))


@auth.route('/register', methods=['GET', 'POST'])
@redirect_if_logged
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

        # If account wasn't activated, new registration is accepted
        if user is not None and user.is_activated == 0:
            db.session.delete(user)
            db.session.commit()
            user = None

        if user is None:
            hashed_password = sha256_crypt.hash(password)
            user = Users(barcode=barcode, first_name=first_name, last_name=last_name, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            token = url_serializer.dumps(barcode, salt=getenv('SECRET_KEY_BARCODE_CONFIRM'))
            token_link = url_for('auth.confirm_email', token=token, _external=True)

            email = barcode + '@astanait.edu.kz'
            send_email(email, token_link)

            flash('User was successfully created!', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('Barcode is already registered', 'danger')
    else:
        flash('Passwords does not match', 'danger')

    return render_template('register.html')


@auth.route('/logout', methods=['GET'])
def logout():
    if session.get('user'):
        del session['user']

    return redirect(url_for('auth.login'))


@auth.route('/confirm-email/<token>')
def confirm_email(token: str):
    try:
        barcode = url_serializer.loads(token, salt=getenv('SECRET_KEY_BARCODE_CONFIRM'), max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    except BadTimeSignature:
        return '<h1>This isn\'t the right token</h1>'

    user = Users.query.filter_by(barcode=barcode).first()
    user.is_activated = True
    db.session.commit()

    flash('User was successfully activated!', 'success')

    return redirect(url_for('auth.login'))
