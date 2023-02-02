"""
this file should be used to get and set game state in database
"""

from google.cloud import firestore

db = firestore.Client(project='battleship-375000')
init_player_state = {"ship_positions": None, "missiles": []}


def get_game(room_id):
    doc_ref = db.collection('battleship').document(room_id)
    game_state = doc_ref.get().to_dict()
    return game_state


def set_game(room_id, game_state):
    doc_ref = db.collection('battleship').document(room_id)
    doc_ref.set(game_state)
