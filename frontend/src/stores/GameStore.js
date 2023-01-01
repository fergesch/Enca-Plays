import { defineStore } from "pinia";
import { fill_gaps, locations_equal, check_collisions } from "@/utils/Utils";

export const useGameStore = defineStore("GameStore", {
  state: () => {
    return {
      socketObj: Object,
      username: "",
      room: "",
      showModal: false,
      modalMessage: "TEST",
      modalBlocking: false,
      gamePhase: "Setup",
      gameSubPhase: "Carrier Start",
      // values of setup ships, playerX turn, win, lose (playerX turn will allow same event to be sent and can validate on username)
      // can make more specific for setup phase to say ship X start, ship X end, confirm (do modal)
      // need value for waiting until both players have set and confirmed ship locations
      // when a player confirms their ship locations we can set a "READY" value in the backend to TRUE
      // check for both "READY" values to be true before moving into PLAYERX turn

      // Variables for the setup phase and ship setting
      shipStart: [],
      shipEnd: [],

      shipPositions: [
        {
          ship: "Carrier",
          locs: [],
          // 'locs': [[1, 5],[2, 5],[3, 5],[4, 5],[5, 5]]
        },
        {
          ship: "Battleship",
          locs: [],
          // 'locs': [[7, 5],[7, 6],[7, 7],[7, 8]]
        },
        {
          ship: "Submarine",
          locs: [],
          // 'locs': [[3, 1],[4, 1],[5, 1]]
        },
        {
          ship: "Cruiser",
          locs: [],
          // 'locs': [[9, 2],[9, 3],[9, 4]]
        },
        {
          ship: "Destroyer",
          locs: [],
          // 'locs': [[0, 0],[0, 1]]
        },
      ],
      myMissiles: [
        [1, 1, true], // this should be 0 indexed
        [8, 4, false],
      ],
      oppMissiles: [
        // [9, 9, true],
        // [5, 6, false],
        // [2, 1, false],
      ],
    };
  },

  getters: {
    occupiedLocations(state) {
      let occupied_locations = [];
      state.shipPositions.forEach(function (ship) {
        ship.locs.forEach(function (loc) {
          occupied_locations.push(loc);
        });
      });
      return occupied_locations
    },

    eligEnds(state) {
      if (!state.gameSubPhase.includes("End")) {
        return [];
      }
      var shipOptions,
        currShip,
        shipLength,
        a,
        b,
        possOptions,
        endOptions,
        occupied_locations;
      shipOptions = {
        Carrier: 5,
        Battleship: 4,
        Submarine: 3,
        Cruiser: 3,
        Destroyer: 2,
      };
      currShip = state.gameSubPhase.split(" ")[0];
      shipLength = shipOptions[currShip] - 1;
      a = state.shipStart[0];
      b = state.shipStart[1];
      possOptions = [
        [a + shipLength, b],
        [a - shipLength, b],
        [a, b + shipLength],
        [a, b - shipLength],
      ];
      endOptions = [];

      // check for collisions
      occupied_locations = this.occupiedLocations
      possOptions.forEach(function (loc) {
        let full_length = fill_gaps([a, b], loc);
        let keep_value = true;
        full_length.forEach(function (ship_loc) {
          let index = check_collisions(occupied_locations, ship_loc);
          if (index >= 0) {
            keep_value = false;
          }
        });
        if (keep_value) {
          endOptions.push(loc);
        }
      });
      return endOptions;
    },

    tempShip(state) {
      if (state.shipStart.length > 0 && state.shipEnd.length > 0) {
        return fill_gaps(state.shipStart, state.shipEnd);
      }
      return [];
    },

    myBoard(state) {
      var matrix = [];
      for (var i = 0; i <= 9; i++) {
        matrix[i] = [];
        for (var j = 0; j <= 9; j++) {
          // set to nothing/ocean
          matrix[i][j] = 0;

          // condition for start position during setup phase
          if (state.shipStart[0] == i && state.shipStart[1] == j) {
            matrix[i][j] = 5;
          }
          // condition for end ship during setup phase
          this.eligEnds.forEach(function (loc) {
            if (loc[0] == i && loc[1] == j) {
              matrix[i][j] = 4;
            }
          });
          // set ship positions
          state.shipPositions.forEach(function (ship) {
            ship["locs"].forEach(function (loc) {
              if (loc[0] == i && loc[1] == j) {
                matrix[i][j] = 1;
              }
            });
          });
          // set hits and misses
          state.oppMissiles.forEach(function (missile) {
            if (missile[0] == i && missile[1] == j) {
              matrix[i][j] = missile[2] ? 2 : 3;
            }
          });
          // set temp ship
          this.tempShip.forEach(function (loc) {
            if (loc[0] == i && loc[1] == j) {
              matrix[i][j] = 4;
            }
          });
        }
      }
      console.log(matrix);
      return matrix;
    },

    oppBoard(state) {
      var matrix = [];
      for (var i = 0; i <= 9; i++) {
        matrix[i] = [];
        for (var j = 0; j <= 9; j++) {
          matrix[i][j] = 0;
          state.myMissiles.forEach(function (missile) {
            if (missile[0] == i && missile[1] == j) {
              matrix[i][j] = missile[2] ? 2 : 3;
            }
          });
        }
      }
      console.log(matrix);
      return matrix;
    },
  },

  actions: {
    create_game_event() {
      this.socketObj.emit("create_room", { username: this.username });
    },
    join_game_event() {
      this.socketObj.emit("join", { room: this.room, username: this.username });
    },
    button_click_event(i, j) {
      this.socketObj.emit("grid_click", { i: i, j: j });
    },

    recieve_room(room) {
      this.room = room;
    },

    start_ship_event(i, j) {
      // check that i,j isn't already in shipLocs
      let index = check_collisions(this.occupiedLocations, [i,j])
      if (index == -1) {
        this.shipStart = [i, j];
        this.gameSubPhase = this.gameSubPhase.split(" ")[0] + " End";
      }
      
    },
    end_ship_event(i, j) {
      // if (this.eligEnds.includes([i, j])) { // this doesnt work because [x,y] !== [x,y]
      var eligEndsStr = JSON.stringify(this.eligEnds);
      var locStr = JSON.stringify([i, j]);
      var c = eligEndsStr.indexOf(locStr);
      if (c != -1) {
        this.shipEnd = [i, j];
        this.gameSubPhase = this.gameSubPhase.split(" ")[0] + " Confirm";
      } else {
        console.log("Bad endpoint");
      }
    },

    submit_ships() {
      this.socketObj.emit("submit_ships", {
        username: this.username,
        room: this.room,
        shipPositions: this.shipPositions,
      });
      this.gamePhase = "Waiting"
      this.gameSubPhase = ""
      this.showModal = true
      this.modalMessage = "Waiting for other player"
      this.modalBlocking = true
    },
  },
});
