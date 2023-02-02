"""
This functions in this file should take in the state and return the modified state or values
"""

init_player_state = {"ship_positions": None, "missiles": []}


def initialize_game(username, room_id):
    game_state = {"players": {},
                  "phase": {}}
    game_state["players"][username] = init_player_state
    game_state["phase"]["primary"] = "Setup"
    game_state["phase"]["secondary"] = ""  # waiting for player 2
    return game_state


def get_players(game_state):
    return list(game_state['players'].keys())


# maybe deal with uniqueness by using sessionId
def add_player(username, game_state):
    game_state["players"][username] = init_player_state
    return game_state


def place_player_ships(username, game_state, ship_locations):
    ship_locs = [{"a": loc[0], "b": loc[1]}
                 for ship in ship_locations for loc in ship['locs']]
    game_state["players"][username]["ship_positions"] = ship_locs
    return game_state


def check_missile(username, game_state, location):
    opp_name = get_opp_name(username, game_state)
    missiles = game_state['players'][username]['missiles']
    opp_ships = game_state['players'][opp_name]['ship_positions']
    hit = False
    loc_dict = {"a": location[0], "b": location[1]}
    try:
        idx = opp_ships.index(loc_dict)
        opp_ships.pop(idx)
        hit = True
    except ValueError:
        pass
    location.append(hit)
    loc_dict['hit'] = hit
    missiles.append(loc_dict)
    return game_state, location


def check_win(username, game_state):
    opp_name = get_opp_name(username, game_state)
    return len(game_state['players'][opp_name]['ship_positions']) == 0


def update_game_phase(game_state, primary, secondary):
    game_state["phase"]["primary"] = primary
    game_state["phase"]["secondary"] = secondary
    return game_state


def get_opp_name(username, game_state):
    return [i for i in list(game_state["players"].keys()) if i != username][0]

# def delete_game(room_id):
#     del GAME_STATES[room_id]
