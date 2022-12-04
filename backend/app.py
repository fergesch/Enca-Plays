from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, send, emit
import logging

LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')


@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)
    

if __name__ == '__main__':
    socketio.run(app, debug=True)