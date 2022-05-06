from utils.PicturesDB import PicturesDB
from flask import session, redirect, url_for
import functools

picturesDB = PicturesDB()


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper
