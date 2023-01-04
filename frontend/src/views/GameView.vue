<script>
import GameBoard from "@/components/GameBoard.vue";
import { useGameStore } from "@/stores/GameStore";
import { next_ship, fill_gaps, get_ship } from "@/utils/Utils";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  components: {
    GameBoard,
  },
  methods: {
    endSubPhase() {
      let curr_phase = this.gameStore.phase["secondary"];
      let ship = get_ship(curr_phase);
      // assign values in store
      let ship_locs = fill_gaps(
        this.gameStore.shipStart,
        this.gameStore.shipEnd
      );
      let ships = [...this.gameStore.shipPositions];
      ships.forEach(function (ship_value, index) {
        if (ship_value.ship == ship) {
          ships[index]["locs"] = ship_locs;
        }
      });
      this.gameStore.shipPositions = ships;

      // moving to next phase and clearing out state
      this.gameStore.shipEnd = [];
      this.gameStore.shipStart = [];
      let next_sub_phase = next_ship(curr_phase);
      this.gameStore.phase["secondary"] = next_sub_phase;
    },
    resetSubPhase() {
      let curr_phase = this.gameStore.phase["secondary"];
      let ship = get_ship(curr_phase);
      this.gameStore.shipEnd = [];
      this.gameStore.shipStart = [];
      this.gameStore.phase["secondary"] = ship + " Start";
    },
  },
};
</script>

<template>
  <div class="game">
    <!-- https://fonts.google.com/icons?selected=Material+Icons&icon.query=user -->
    <div class="player-chips">
      <q-chip icon="person" :label="gameStore.username" />
      <q-chip icon="room" :label="gameStore.room" />
    </div>
    <div v-if="gameStore.shipText">Set ships {{ gameStore.shipText }}</div>

    <GameBoard board="oppBoard" />
    <br />
    <GameBoard board="myBoard" />

    <button
      v-if="this.gameStore.phase['secondary'].includes('Confirm')"
      @click="endSubPhase"
    >
      Confirm Ship
    </button>
    <button
      v-if="this.gameStore.phase['secondary'].includes('End') || this.gameStore.phase['secondary'].includes('Confirm')"
      @click="resetSubPhase"
    >
      Reset Current Ship
    </button>
    <button
      v-if="this.gameStore.phase['secondary'] == 'Submit Ships'"
      @click="this.gameStore.submit_ships()"
    >
      Submit Ships
    </button>
    <!-- Add button or buttons to reset ship if you dont want to submit -->
  </div>
</template>

<style></style>
