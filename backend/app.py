from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import logging

LOGGER = logging.getLogger(__name__)
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins='*')

@socketio.on('my event')
def handle_my_custom_event(json):
    LOGGER.info("custom event", json)
    print('received json: ' + str(json))

if __name__ == '__main__':
    socketio.run(app)