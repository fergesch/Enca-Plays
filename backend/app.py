from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
import random

LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')

# Deal with people disconnecting -- close room?

def get_rooms():
    manager = socketio.server.manager
    print(manager.rooms)
    rooms = manager.rooms["/"]
    response = {k: len(v) for k, v in rooms.items()}
    return response


def join_room_action(username, room):
    room = str(room)
    join_room(room)
    print(username + ' has entered the room.')
    emit('joined', {'username': username, 'room': room}, to=room)


@socketio.on('create_room')
def on_create_room(data):
    username = data['username']
    rooms = get_rooms()
    room = random.randint(1,999)
    while room in rooms.keys():
        room = random.randint(1,999)
    join_room_action(username, room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    rooms = get_rooms()
    if room not in rooms.keys():
        emit("modal_event", {"room": room, "message": "Room does not exist. Enter another room or create new game."})
    elif rooms[room] >= 2:
        emit("modal_event", {"room": room, "message": "Too many players in that room"})
    else:
        join_room_action(username, room)


@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)