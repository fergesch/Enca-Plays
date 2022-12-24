
GAME_STATES = {}
GAME_DIMENSION = 10
PLAYER_ONE = "player1"
PLAYER_TWO = "player2"
BOARD_ONE = "board1"
BOARD_TWO = "board2"
NOTHING = 0
SHIP = 1
HIT = 2
MISS = 3


def set_player_ship_board(username, room_id, tmp_board):
  game_state = GAME_STATES[room_id]
  player_value = game_state[username]
  board_value =  BOARD_ONE if player_value == PLAYER_ONE else BOARD_TWO
  game_state[board_value] = tmp_board


def get_player_ship_board(username, room_id):
  game_state = GAME_STATES[room_id]
  player_value = game_state[username]
  return game_state[BOARD_ONE] if player_value == PLAYER_ONE else game_state[BOARD_TWO]
  

def get_player_missile_board(username, room_id):
  game_state = GAME_STATES[room_id]
  player_value = game_state[username]
  return game_state[BOARD_TWO] if player_value == PLAYER_ONE else game_state[BOARD_ONE]
  

def place_player_ships(username, room_id, ship_locations):
  tmp_board = [[0 for x in range(GAME_DIMENSION)] for y in range(GAME_DIMENSION)]
  for ship_loc in ship_locations:
    for loc in ship_loc:
      tmp_board[loc[0]][loc[1]] = SHIP
  set_player_ship_board(username, room_id, tmp_board)


def initialize_game(username, room_id):
    game_state = {BOARD_ONE: None,
                  BOARD_TWO: None,
                  username: PLAYER_ONE}
    GAME_STATES[room_id] = game_state


# maybe deal with uniqueness by using sessionId
def add_player(username, room_id):
    GAME_STATES[room_id][username] = PLAYER_TWO