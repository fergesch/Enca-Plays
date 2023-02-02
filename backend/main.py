import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
import logging
import uuid
import firestore as fs
import board_actions as ba

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


def join_room_action(username, room, game_state):
    join_room(room)
    print(username + ' has entered the room.')
    fs.set_game(room, game_state)
    emit('joined', {'username': username, 'room': room}, to=room)


@socketio.on('create_room')
def on_create_room(data):
    username = data['username']
    room = uuid.uuid4().hex
    room = str(room)
    game_state = ba.initialize_game(username, room)
    join_room_action(username, room, game_state)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    rooms = get_rooms()
    if room not in rooms.keys():
        emit("modal_event", {
             "room": room, "message": "Room does not exist. Enter another room or create new game."})
        return None
    elif rooms[room] >= 2:
        emit("modal_event", {"room": room,
             "message": "Too many players in that room"})
        return None
    game_state = fs.get_game(room)
    if username in ba.get_players(game_state):
        emit("modal_event", {
             "room": room, "message": "Name already in use. Pick a different username"})
    else:
        game_state = ba.add_player(username, game_state)
        join_room_action(username, room, game_state)


@socketio.on("submit_ships")
def submit_ships(data):
    ship_positions = data["shipPositions"]
    username = data['username']
    room = data['room']
    game_state = fs.get_game(room)
    game_state = ba.place_player_ships(username, game_state, ship_positions)
    player_keys = ba.get_players(game_state)
    ready_count = [k for k in player_keys if game_state["players"][k]["ship_positions"] is not None]
    if len(ready_count) == 2:
        game_state = ba.update_game_phase(game_state, "Playing", player_keys[0])
        emit("players_ready", game_state['phase'], to=room)
    fs.set_game(room, game_state)

@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)


@socketio.on('fire_missile')
def fire_missile(data):
    username = data["username"]
    room = data["room"]
    loc = data["loc"]
    game_state = fs.get_game(room)
    opp_name = ba.get_opp_name(username, game_state)
    game_state, missile_result = ba.check_missile(username, game_state, loc)
    game_state = ba.update_game_phase(game_state, "Playing", opp_name)
    emit('return_missile', {"username": username,
         "loc": missile_result, "phase": game_state['phase']}, to=room)
    if (ba.check_win(username, game_state)):  # player wins
        game_state = ba.update_game_phase(game_state, "Game Over", username)
        print('Winner')
        emit("modal_event", {"room": room,
             "message": f"{username} WINS!"}, to=room)
        # ba.delete_game(room)
        # requests.get('http://127.0.0.1:5001/end', params={"room": room})
    fs.set_game(room, game_state)


@socketio.on('disconnect')
def disconnect():
    # should check what connections we have and room exist
    # compare that with what is in GAME_STATES
    # cleanup when necessary
    print('User disconnect')


@socketio.on('kill_button')
def kill_button():
    print('KILL KILL KILL')
    socketio.stop()
    print('I am DEAD')


@app.route('/health', methods=['GET'])
def health_check():
    print("Hello World")
    # socketio.run(app, debug=True)
    socketio.stop()
    return "Hello World"

# @app.route('/fetch_rooms', methods=['GET'])
# def fetch_rooms():
#     return str(get_rooms())

# @app.route('/fetch_game_states', methods=['GET'])
# def fetch_game_states():
#     return GAME_STATES


if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # app.run(debug=True)
