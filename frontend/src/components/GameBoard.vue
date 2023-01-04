<script>
import { useGameStore } from "@/stores/GameStore";
import GameRow from "./GameRow.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  // name: "Board",
  props: ["board"],

  components: {
    GameRow,
  },
};
</script>

<template>
  <!-- make header for letters ABC... -->
  <GameRow v-for="i in 10" :rowNum="i - 1" :board="board" />
</template>
