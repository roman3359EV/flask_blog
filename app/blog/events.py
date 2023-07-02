from flask_socketio import SocketIO, emit, send, join_room
from flask_login import current_user

socketio = SocketIO()


class BlogEvents(object):
    def __init__(self, info):
        self.info = info

    def front_my_event(self, message):
        print(f"{self.info} - frontend {message}")

    def backend_event_broadcast(self, message):
        print(f"{self.info} - backend broadcast {message}")
        emit('backend_my_event', {"data": message}, namespace='/', broadcast=True)

    def backend_event(self, message, room):
        print(f"{self.info} - backend {message}")
        emit('backend_my_private_event', {"data": message}, namespace='/', room=room)

    def join(self, login):
        room = f"private_room_{login}"
        print(f"{self.info} - joined {room}")
        join_room(room)
        emit('backend_my_private_event', 'you joined in private room', namespace='/', room=room)


events = BlogEvents('ws channel')


@socketio.on('front_my_event', namespace='/')
def front_my_event(message):
    events.front_my_event(message)


@socketio.on('join', namespace='/')
def join():
    events.join(current_user.login)


def backend_my_event(message=''):
    events.backend_event_broadcast(message)


def backend_my_private_event(message='', room=''):
    print(room)
    events.backend_event(message, room)
