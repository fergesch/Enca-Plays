from flask import Flask, request
from flask_cors import CORS

# from socket_client import SocketClient
import cpu_player

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return("<p>Hello, World!</p>")

# create a new socketio connection
@app.route("/create")
def create():
    room=request.args.get('room')
    cpu_player.initialize_cpu(room)
    return('CPU created')

@app.route("/end")
def end():
    # For each CPU player, close the Socketio connection and then delete the entry in PLAYER_STATES
    print("Req kill")
    room=request.args.get('room')
    cpu_player.end_game(room)
    return('game over')

if __name__ == "__main__":
    app.run(debug=True)