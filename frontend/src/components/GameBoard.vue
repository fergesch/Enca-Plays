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
