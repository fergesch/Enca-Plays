<script>
import { useGameStore } from "@/stores/GameStore";
import gameCell from "./gameCell.vue";
import {next_ship, fill_gaps} from "@/utils/Utils";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  name: "Board",
  methods: {
    endSubPhase() {
      let curr_phase = this.gameStore.gameSubPhase
      let ship = curr_phase.split(" ")[0]
      // assign values in store
      let ship_locs = fill_gaps(this.gameStore.shipStart, this.gameStore.shipEnd)
      let ships = [...this.gameStore.shipPositions]
      ships.forEach(function (ship_value, index) {
        if (ship_value.ship == ship) {
          ships[index]["locs"] = ship_locs
        }
      })
      this.gameStore.shipPositions = ships
      // let next_sub_phase = next_ship(curr_phase);
      // this.gameStore.gameSubPhase = next_sub_phase;
      // moving to next phase and clearing out state
      this.gameStore.shipEnd = [];
      this.gameStore.shipStart = [];
      let next_sub_phase = next_ship(curr_phase);
      this.gameStore.gameSubPhase = next_sub_phase;
    },
    resetSubPhase() {
      let curr_phase = this.gameStore.gameSubPhase
      let ship = curr_phase.split(" ")[0]
      this.gameStore.shipEnd = [];
      this.gameStore.shipStart = [];
      this.gameStore.gameSubPhase = ship + " Start"     
    },
  },

  components: {
    gameCell,
  },

  // computed: {
  //   hitMap() {
  //     var matrix = [];
  //     for (var i = 0; i <= 9; i++) {
  //       matrix[i] = [];
  //       for (var j = 0; j <= 9; j++) {
  //         matrix[i][j] = "ocean";
  //         this.gameStore.myMissiles.forEach(function (missile) {
  //           if (missile[0] == i && missile[1] == j) {
  //             matrix[i][j] = missile[2] ? "hit" : "miss";
  //           }
  //         });
  //       }
  //     }
  //     console.log(matrix);
  //     return matrix;
  //   },
  // },
};
</script>

<template>
  <div class="oppBoard">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <gameCell
          :val="this.gameStore.oppBoard[i - 1][j - 1]"
          :loc="[i - 1, j - 1]"
          board="oppBoard"
        />
        <!-- <gameCell :val="this.hitMap[i - 1][j - 1]" :loc="[i - 1, j - 1]" board="oppBoard"/> -->
      </div>
    </div>
  </div>
  <br />
  <div class="myBoard">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <gameCell
          :val="this.gameStore.myBoard[i - 1][j - 1]"
          :loc="[i - 1, j - 1]"
          board="myBoard"
        />
      </div>
    </div>
  </div>
  <!-- make a button that shows up in the SHIP Confirm subphase that sets shipPosition and moves to next ship -->
  <button
    v-if="this.gameStore.gameSubPhase.includes('Confirm')"
    @click="endSubPhase"
  >
    Confirm Ship
  </button>
  <button
    v-if="this.gameStore.gameSubPhase.includes('Confirm')"
    @click="resetSubPhase"
  >
    Reset Current Ship
  </button>
  <button
    v-if="this.gameStore.gameSubPhase == 'Submit Ships'"
    @click="this.gameStore.submit_ships()"
  >
    Submit Ships
  </button>
</template>

<style>
.cell {
  width: 30px;
  height: 30px;
}
</style>
