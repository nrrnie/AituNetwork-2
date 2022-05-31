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

    if user is None or sha256_crypt.verify(password, user.password) is False:
        flash('Barcode or password is wrong', 'danger')

    if user is not None and user.is_activated is False:
        flash('User is not activated yet. Check your email.', 'danger')
    elif user is not None and sha256_crypt.verify(password, user.password):
        session['user'] = user
        return redirect(url_for('main.home'))

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
            header = 'Email verification'
            message = 'Your verification link is %s'
            send_email(email, token_link, header, message)

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


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot-password.html')

    barcode = request.form.get('barcode')

    token = url_serializer.dumps(barcode, salt=getenv('SECRET_KEY_PASSWORD_RECOVER'))
    token_link = url_for('auth.recover_password', token=token, _external=True)

    email = barcode + '@astanait.edu.kz'
    header = 'Password recovery'
    message = 'Your link for password recovery is %s'
    send_email(email, token_link, header, message)

    flash('Link was sent to your email', 'success')
    return redirect(url_for('auth.login'))


@auth.route('/recover-password/<token>', methods=['GET', 'POST'])
def recover_password(token: str):
    try:
        barcode = url_serializer.loads(token, salt=getenv('SECRET_KEY_PASSWORD_RECOVER'), max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired!</h1>'
    except BadTimeSignature:
        return '<h1>This isn\'t the right token</h1>'

    if request.method == 'GET':
        return render_template('recover-password.html')

    password = request.form.get('new-password')
    password_confirm = request.form.get('new-password-confirm')

    if password != password_confirm:
        flash('Passwords does not match', 'danger')
        return redirect(url_for('auth.recover_password', token=token))

    update_info = dict(password=sha256_crypt.hash(password))
    Users.update_user_info_by_barcode(barcode, update_info)

    flash('Password was recovered', 'success')
    return redirect(url_for('auth.login'))
