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

def get_rooms(username):
    manager = socketio.server.manager
    print(username, manager.rooms)
    rooms = manager.rooms["/"]
    return rooms.keys()


def join_room_action(username, room):
    
    room = str(room)
    join_room(room)
    print(username + ' has entered the room.')
    emit('joined', {'username': username, 'room': room}, to=room)


@socketio.on('create_room')
def on_create_room(data):
    username = data['username']
    room = random.randint(1,999)
    join_room_action(username, room)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    rooms = get_rooms(username)
    if room not in rooms:
        emit("room_no_exists", {"room": room}) # Handle this event on the front end, make modal 
    else:
        join_room_action(username, room)


@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)