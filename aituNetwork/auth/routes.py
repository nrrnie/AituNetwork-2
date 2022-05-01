from aituNetwork.auth import auth


@auth.route('/login', methods=['GET'])
def login():
    return 'login'
