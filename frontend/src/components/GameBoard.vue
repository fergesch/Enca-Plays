<script>
import { useGameStore } from "@/stores/GameStore";
import { LETTERS } from "@/utils/Utils";
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
  data() {
    return {
      letters: LETTERS,
    };
  },
};
</script>

<template>
  <!-- make header for letters ABC... -->
  <div v-for="letter in letters" class="boardCell">{{ letter }}</div>
  <br />
  <GameRow v-for="i in 10" :rowNum="i - 1" :board="board" />
</template>

<style>
.boardCell {
  width: 35px;
  height: 35px;
  text-align: center;
  display: inline-block;
}
</style>
