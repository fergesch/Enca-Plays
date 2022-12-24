<!-- NEXT STEPS: Place ships
  Will need to store ships & sizes somewhere
FLOW: go one ship at a time. Click starting cell, highlight endpoints. Click endpoint
Hit confirm button before moving to next ship
Once all ships placed use submit_ships feature -->

<script>
import GameBoard from "@/components/GameBoard.vue";
import { useGameStore } from "@/stores/GameStore";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  components: {
    GameBoard,
  },
};
</script>

<template>
  <div class="about">
    <!-- https://fonts.google.com/icons?selected=Material+Icons&icon.query=user -->
    <div class="player-chips">
      <q-chip icon="person" :label="gameStore.username" />
      <q-chip icon="room" :label="gameStore.room" />
    </div>

    <GameBoard />
    <button @click="this.gameStore.submit_ships()">Submit Ships</button>
  </div>
</template>

<style>
/* .player-class {

} */
/* @media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
} */
</style>
