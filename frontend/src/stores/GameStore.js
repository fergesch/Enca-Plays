import { defineStore } from "pinia";
// import { fiveLetter, toggleMatch, checkWord } from "../utils/Utils";
// import Api from "../utils/Api.vue";
// import { ref, computed } from "vue";

export const useGameStore = defineStore("GameStore", {
  state: () => {
    return {
      socketObj: Object,
      username: "",
      room: "",
      showModal: false,
      modalMessage: "TEST",
      shipPositions: [
        // check for overlaps somewhere
        [
          [1, 5],
          [2, 5],
          [3, 5],
          [4, 5],
          [5, 5],
        ],
        [
          [6, 5],
          [6, 6],
          [6, 7],
          [6, 8],
        ],
        [
          [3, 1],
          [4, 1],
          [5, 1],
        ],
        [
          [9, 2],
          [9, 3],
          [9, 4],
        ],
        [
          [0, 0],
          [0, 1],
        ],
      ],
      myMissiles: [
        [1, 1, true], // this should be 0 indexed
        [8, 4, false],
      ],
      oppMissiles: [
        [10, 10, true],
        [5, 6, false],
        [2, 1, false],
      ],
    };
  },

  // getters: {
  //   doubleCount: (state) => state.count * 2,
  // },

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
    submit_ships() {
      this.socketObj.emit("submit_ships", {
        username: this.username,
        room: this.room,
        locations: this.shipPositions,
      });
    },
    // changeMatch(loc) {
    //   // given position of letter [ith word, jth letter] want to flip between -1,0,1
    //   Object.values(this.words[loc[0]]).forEach((value) => {
    //     value.forEach(function (item) {
    //       if (item[0] == loc[1]) {
    //         item[1] = toggleMatch(item[1]);
    //       }
    //     });
    //   });
    // },

    // async addWord() {
    //   let word = fiveLetter(this.currentWord.slice());
    //   if (word) {
    //     let check = await checkWord(word);
    //     if (check) {
    //       let letterList = word.split("");

    //       const letterMap = {};
    //       letterList.forEach(function (item, index) {
    //         if (!(item in letterMap)) {
    //           letterMap[item] = [];
    //         }
    //         letterMap[item].push([index, -1]);
    //       });

    //       this.words.push(letterMap);
    //       this.currentWord = ""; //set back to empty for next input
    //     } else {
    //       this.showModal = true;
    //     }
    //   } else {
    //     this.showModal = true;
    //   }
    // },

    // removeWord(n) {
    //   let wordList = [...this.words];
    //   wordList.splice(n, 1);
    //   this.words = wordList;
    // },

    // getWord() {
    //   Api.post("/word", this.words)
    //     .then((response) => {
    //       // console.log(response)
    //       this.recoWord = response["data"];
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // },
  },
});
