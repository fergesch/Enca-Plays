
GAME_STATES = {}
PLAYER_ONE = "player1"
PLAYER_TWO = "player2"
NOTHING = 0
SHIP = 1
HIT = 2
MISS = 3


def initialize_player_state(username, player_num):
	return { 
		username: {
			"player_num": player_num,
			"ship_positions": None,
			"missiles": []
	}}

def place_player_ships(username, room_id, ship_locations):
	ship_locs = [loc for ship in ship_locations for loc in ship['locs']]
	GAME_STATES[room_id][username]["ship_positions"] = ship_locs


def initialize_game(username, room_id):
	game_state = initialize_player_state(username, PLAYER_ONE)
	game_state["game_phase"] = "setup"
	GAME_STATES[room_id] = game_state


# maybe deal with uniqueness by using sessionId
def add_player(username, room_id):
	GAME_STATES[room_id].update(initialize_player_state(username, PLAYER_TWO))
