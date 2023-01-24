from google.cloud import firestore

db = firestore.Client(project='battleship-375000')
init_player_state = {"ship_positions": None, "missiles": []}


def get_game(room_id):
    doc_ref = db.collection('battleship').document(room_id)
    game_state = doc_ref.get().to_dict()
    return (doc_ref, game_state)


def place_player_ships(username, room_id, ship_locations):
    doc_ref, game_state = get_game(room_id)
    ship_locs = [{"a": loc[0], "b": loc[1]}
                 for ship in ship_locations for loc in ship['locs']]
    game_state["players"][username]["ship_positions"] = ship_locs
    doc_ref.set(game_state)


def initialize_game(username, room_id):
    game_state = {"players": {},
                  "phase": {}}
    game_state["players"][username] = init_player_state
    game_state["phase"]["primary"] = "Setup"
    game_state["phase"]["secondary"] = ""  # waiting for player 2
    # GAME_STATES[room_id] = game_state
    doc_ref = db.collection(u'battleship').document(room_id)
    doc_ref.set(game_state)


def get_players(room_id):
    _, game_state = get_game(room_id)
    return game_state['players'].keys()


# maybe deal with uniqueness by using sessionId
def add_player(username, room_id):
    doc_ref, game_state = get_game(room_id)
    game_state["players"][username] = init_player_state
    doc_ref.set(game_state)


def check_missile(username, room_id, location):
    doc_ref, game_state = get_game(room_id)
    opp_name = get_opp_name(username, room_id)
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
    doc_ref.set(game_state)
    return location


def check_win(username, room_id):
    _, game_state = get_game(room_id)
    opp_name = get_opp_name(username, room_id)
    return len(game_state['players'][opp_name]['ship_positions']) == 0


def update_game_phase(room_id, primary, secondary):
    doc_ref, game_state = get_game(room_id)
    game_state["phase"]["primary"] = primary
    game_state["phase"]["secondary"] = secondary
    doc_ref.set(game_state)
    return game_state["phase"]


def get_opp_name(username, room_id):
    _, game_state = get_game(room_id)
    return [i for i in list(game_state["players"].keys()) if i != username][0]

# def delete_game(room_id):
#     del GAME_STATES[room_id]
