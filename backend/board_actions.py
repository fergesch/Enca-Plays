
GAME_STATES = {}
PLAYER_ONE = "player1"
PLAYER_TWO = "player2"


def initialize_player_state(player_num):
    return {
        "player_num": player_num,
        "ship_positions": None,
        "missiles": []
    }


def place_player_ships(username, room_id, ship_locations):
    ship_locs = [loc for ship in ship_locations for loc in ship['locs']]
    GAME_STATES[room_id]["players"][username]["ship_positions"] = ship_locs


def initialize_game(username, room_id):
    game_state = {"players": {},
                  "phase": {}}
    game_state["players"][username] = initialize_player_state(PLAYER_ONE)
    game_state["phase"]["primary"] = "Setup"
    game_state["phase"]["secondary"] = ""  # waiting for player 2
    GAME_STATES[room_id] = game_state


# maybe deal with uniqueness by using sessionId
def add_player(username, room_id):
    GAME_STATES[room_id]["players"][username] = initialize_player_state(PLAYER_TWO)
    # update game subphase to be


def check_missile(username, room_id, location):
    opp_name = get_opp_name(username, room_id)
    game_state = GAME_STATES[room_id]
    missiles = game_state['players'][username]['missiles']
    opp_ships = game_state['players'][opp_name]['ship_positions']
    hit = False
    try:
        idx = opp_ships.index(location)
        opp_ships.pop(idx) 
        hit = True
    except ValueError:
        pass
    location.append(hit)
    missiles.append(location)
    return location

def check_win(username, room_id):
    game_state = GAME_STATES[room_id]
    opp_name = get_opp_name(username, room_id)
    return len(game_state['players'][opp_name]['ship_positions']) == 0


def update_game_phase(room_id, primary, secondary):
	game_state = GAME_STATES[room_id]
	game_state["phase"]["primary"] = primary
	game_state["phase"]["secondary"] = secondary
	return game_state["phase"]

def get_opp_name(username, room_id):
    game_state = GAME_STATES[room_id]
    return [i for i in list(game_state["players"].keys()) if i != username][0]

def delete_game(room_id):
    del GAME_STATES[room_id]