from aitu_network_app import socketio


@socketio.on('event')
def handle_message(data):
    print(data)
