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
  <div class="game">
    <!-- https://fonts.google.com/icons?selected=Material+Icons&icon.query=user -->
    <div class="player-chips">
      <q-chip icon="person" :label="gameStore.username" />
      <q-chip icon="room" :label="gameStore.room" />
    </div>

    <GameBoard />
  </div>
</template>

<style>
/* .player-class {

} */
/* @media (min-width: 1024px) {
  .game {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
} */
</style>
