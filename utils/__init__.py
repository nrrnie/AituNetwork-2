from utils.PicturesDB import PicturesDB
from flask import session, redirect, url_for
from email.message import EmailMessage
from smtplib import SMTP_SSL
from os import getenv
import functools

picturesDB = PicturesDB()


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


def send_email(to: str, token_link: str, header: str, msg: str):
    message = EmailMessage()
    message['Subject'] = header
    message['From'] = getenv('SMTP_SENDER')
    message['To'] = to
    message.set_content(msg % token_link)

    with SMTP_SSL('smtp.gmail.com', int(getenv('SMTP_PORT'))) as smtp:
        smtp.login(getenv('SMTP_SENDER'), getenv('SMTP_PASSWORD'))
        smtp.send_message(message)
