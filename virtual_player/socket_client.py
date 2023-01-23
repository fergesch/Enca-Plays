import socketio
from helpers import setup_ships, rand_space

server = 'http://127.0.0.1:5000'


class SocketClient:
    def __init__(self, room, username):
        self.room = room
        self.username = username
        self.sio = socketio.Client()
        self.ship_positions = setup_ships()
        self.missiles = []

        self.sio.connect(server)
        self.sio.emit("join", {"room": self.room, "username": self.username})

        @self.sio.on('joined')
        def on_joined(data):
            if data["username"] == self.username:
                self.sio.emit(
                    "submit_ships",
                    {'username': self.username, 'room': self.room,
                        'shipPositions': self.ship_positions},
                    # room=self.room
                )
            print('I joined!')

        @self.sio.on('players_ready')
        def on_players_ready(data):
            self.fire_missile(data)

        @self.sio.on('return_missile')
        def on_return_missile(data):
            self.fire_missile(data)

    def fire_missile(self, data):
        # Computer's turn
        if data['phase']['secondary'] == self.username:
            next_shot = rand_space(self.missiles)
            self.sio.emit(
                "fire_missile",
                {"room": self.room, "username": self.username, "loc": next_shot}
            )
        # Getting response of this computers shot, other players turn to play
        elif data.get("username", None) == self.username:
            self.missles.append(data["loc"])

    def emit_test(self):
        self.sio.emit("test", {"room": self.room,
                      "message": 'This is a string'})

    def disconnect(self):
        self.sio.disconnect()
