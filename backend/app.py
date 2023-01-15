from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room, leave_room
import logging
import random
import board_actions
from board_actions import GAME_STATES

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
    rooms = get_rooms()
    room = random.randint(1,999)
    while room in rooms.keys():
        room = random.randint(1,999)
    room = str(room)
    board_actions.initialize_game(username, room)
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
    elif username in GAME_STATES[room].keys():
        emit("modal_event", {"room": room, "message": "Name already in use. Pick a different username"})
    else:
        board_actions.add_player(username, room)
        join_room_action(username, room)


@socketio.on("submit_ships")
def submit_ships(data):
    ship_positions = data["shipPositions"]
    username = data['username']
    room = data['room']
    board_actions.place_player_ships(username, room, ship_positions)
    game_state = board_actions.GAME_STATES[room]
    player_keys = list(game_state["players"].keys())
    ready_count = [k for k in player_keys if game_state["players"][k]["ship_positions"] is not None]
    if len(ready_count) == 2:
        event_data = board_actions.update_game_phase(room, "Playing", player_keys[0])
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
    if(board_actions.check_win(username, room)):#player wins
        new_phase = board_actions.update_game_phase(room, "Game Over", username)
        print('Winner')
        emit("modal_event", {"room": room, "message": f"{username} WINS!"}, to=room)
    
    emit('return_missile', {"username": username, "loc": missile_result, "phase": new_phase}, to=room)
    
        


if __name__ == '__main__':
    socketio.run(app, debug=True)