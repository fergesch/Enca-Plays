import { io } from "socket.io-client";

class SocketioService {
  socket;
  constructor() {}

  setupSocketConnection() {
    this.socket = io("ws://127.0.0.1:5000", {
      transports: ["websocket", "polling", "flashsocket"],
    });
    //this.socket.emit('my message', 'Hello there from Vue.');

    // this.socket.on('my broadcast', (data) => {
    //   console.log(data);
    // });
    this.socket.on("after connect", (data) => {
      console.log(data);
    });

    this.socket.on("joined", (data) => {
      console.log(data);
    });
  }

  create_game_event() {
    this.socket.emit("join", { room: 123, username: "Player 1" });
  }

  button_click_event(i, j) {
    this.socket.emit("grid_click", { i: i, j: j });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
    }
  }
}

export default new SocketioService();
