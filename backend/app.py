from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import logging

LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    print(username + ' has entered the room.')
    # send(username + ' has entered the room.', to=room)
    emit('joined', username + ' has entered the room.', to=room)


@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)