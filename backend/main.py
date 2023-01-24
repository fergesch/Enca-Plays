import os
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import requests
import logging
import uuid
import board_actions

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
    join_room(room)
    print(username + ' has entered the room.')
    emit('joined', {'username': username, 'room': room}, to=room)


@socketio.on('create_room')
def on_create_room(data):
    username = data['username']
    room = uuid.uuid4().hex
    room = str(room)
    board_actions.initialize_game(username, room)
    join_room_action(username, room)


@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    rooms = get_rooms()
    if room not in rooms.keys():
        emit("modal_event", {
             "room": room, "message": "Room does not exist. Enter another room or create new game."})
    elif rooms[room] >= 2:
        emit("modal_event", {"room": room,
             "message": "Too many players in that room"})
    elif username in board_actions.get_players(room):
        emit("modal_event", {
             "room": room, "message": "Name already in use. Pick a different username"})
    else:
        board_actions.add_player(username, room)
        join_room_action(username, room)


@socketio.on("submit_ships")
def submit_ships(data):
    ship_positions = data["shipPositions"]
    username = data['username']
    room = data['room']
    board_actions.place_player_ships(username, room, ship_positions)
    _, game_state = board_actions.get_game(room)
    player_keys = list(game_state["players"].keys())
    ready_count = [k for k in player_keys if game_state["players"]
                   [k]["ship_positions"] is not None]
    if len(ready_count) == 2:
        event_data = board_actions.update_game_phase(
            room, "Playing", player_keys[0])
        emit("players_ready", event_data, to=room)


@socketio.on('grid_click')
def handle_my_custom_event(json):
    LOGGER.info("grid click", json)


@socketio.on('fire_missile')
def fire_missile(data):
    username = data["username"]
    room = data["room"]
    loc = data["loc"]
    opp_name = board_actions.get_opp_name(username, room)
    missile_result = board_actions.check_missile(username, room, loc)
    new_phase = board_actions.update_game_phase(room, "Playing", opp_name)
    if (board_actions.check_win(username, room)):  # player wins
        new_phase = board_actions.update_game_phase(
            room, "Game Over", username)
        print('Winner')
        emit("modal_event", {"room": room,
             "message": f"{username} WINS!"}, to=room)
        # board_actions.delete_game(room)
        requests.get('http://127.0.0.1:5001/end', params={"room": room})

    emit('return_missile', {"username": username,
         "loc": missile_result, "phase": new_phase}, to=room)


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
