from socket_client import SocketClient

PLAYER_STATES = {}


def initialize_cpu(room_id, cpus=1):
    tmp_dict = {}
    for i in range(cpus):
        username = f'cpu_{i}'
        tmp_dict[username] = SocketClient(room_id, username)
    PLAYER_STATES[room_id] = tmp_dict

def end_game(room_id):
    print(PLAYER_STATES)
    for cpu in PLAYER_STATES[room_id].values():
        cpu.disconnect()
    del PLAYER_STATES[room_id]
    print(PLAYER_STATES)