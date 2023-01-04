<script>
import { useGameStore } from "@/stores/GameStore";
import { LETTERS } from "@/utils/Utils";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  props: ["val", "loc", "board"],
  methods: {
    clickLog() {
      // need to handle different phases of the game using this.gameStore.gamePhase which will
      console.log(this.loc, this.val, this.board);
      // condition for gamePhase setup and board == myBoard
      if (
        this.board == "myBoard" &&
        this.gameStore.gamePhase == "Setup" &&
        this.gameStore.gameSubPhase.includes("Start")
      ) {
        this.gameStore.start_ship_event(this.loc[0], this.loc[1]);
      } else if (
        this.board == "myBoard" &&
        this.gameStore.gamePhase == "Setup" &&
        this.gameStore.gameSubPhase.includes("End")
      ) {
        this.gameStore.end_ship_event(this.loc[0], this.loc[1]);
      }

      // condition for gamePhase
      if (
        this.board == "oppBoard" &&
        this.gameStore.gamePhase == this.gameStore.username
      ) {
        this.gameStore.button_click_event(this.loc[0], this.loc[1]);
      }
    },
  },
  data() {
    return {
      colorMap: {
        0: "ocean",
        1: "ship",
        2: "hit",
        3: "miss",
        4: "eligEnd",
        5: "shipStart",
      },
      letters: LETTERS,
    };
  },
};
</script>

<template>
  <button :class="colorMap[val]" @click="clickLog" class="boardCell">
    <!-- {{ loc[0].toString() + "|" + loc[1].toString() }} -->
    {{ letters[loc[1] + 1].toString() + (loc[0] + 1).toString() }}
  </button>
</template>

<style scoped>
.hit {
  background-color: red;
  color: red;
}

.miss {
  background-color: white;
  color: white;
}

.ocean {
  background-color: blue;
  color: blue;
}

.ship {
  background-color: grey;
  color: grey;
}

.eligEnd {
  background-color: yellow;
  color: yellow;
}

.shipStart {
  background-color: green;
  color: green;
}

/* button {
  width: 35px;
  height: 35px;
} */
</style>
