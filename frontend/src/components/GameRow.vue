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
  <div class="rowInd">{{ rowNum + 1 }}</div>
  <GameCell
    v-for="j in 10"
    :val="this.gameStore[board][rowNum][j - 1]"
    :loc="[rowNum, j - 1]"
    :board="board"
  />
  <br />
</template>

<style scoped>
.rowInd {
  width: 30px;
  height: 30px;
  text-align: center;
  display: inline-block;
}
</style>
