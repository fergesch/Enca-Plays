<script>
import { useGameStore } from "@/stores/GameStore";
import GameCell from "@/components/GameCell.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  props: ["rowNum", "board"],
  components: {
    GameCell,
  },
};
</script>

<template>
  <div class="boardCell">{{ rowNum + 1 }}</div>
  <GameCell
    v-for="j in 10"
    :val="this.gameStore[board][rowNum][j - 1]"
    :loc="[rowNum, j - 1]"
    :board="board"
    :key="j"
  />
  <br />
</template>

<style scoped></style>
