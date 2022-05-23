from flask import session
from datetime import datetime
from aituNetwork.models import Users
from __main__ import socketio


@socketio.on('connect')
def connect():
    Users.update_user_info(session['user'].id, dict(last_online='now'))


@socketio.on('disconnect')
def disconnect():
    Users.update_user_info(session['user'].id, dict(last_online=str(datetime.now().replace(microsecond=0))))
