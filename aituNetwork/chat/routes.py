from flask import request, session, render_template, url_for
from aituNetwork.chat import chat
from aituNetwork.models import Chats, UsersChats
from utils import auth_required


@chat.route('/<chat_id>')
@auth_required
def chat(chat_id: int):
    user = session['user']

    # user with whom you chat
    chat_user = UsersChats.get_second_chat_user(chat_id, user.id)

    if not Chats.is_chat_exist(chat_id):
        return 'Chat does not exist'

    if not UsersChats.is_user_in_chat(user.id, chat_id):
        return 'User do not have access to this chat'

    if request.method == 'GET':
        return render_template('chat.html', user=user, chat_user=chat_user)

