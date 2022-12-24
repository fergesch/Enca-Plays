<script>
import { useGameStore } from "@/stores/GameStore";
import gameCell from "./gameCell.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  name: "Board",
  components: {
    gameCell,
  },

  computed: {
    hitMap() {
      var matrix = [];
      for (var i = 0; i <= 9; i++) {
        matrix[i] = [];
        for (var j = 0; j <= 9; j++) {
          matrix[i][j] = "ocean";
          this.gameStore.myMissiles.forEach(function (missile) {
            if (missile[0] == i && missile[1] == j) {
              matrix[i][j] = missile[2] ? "hit" : "miss";
            }
          });
        }
      }
      console.log(matrix);
      return matrix;
    },
  },
};
</script>

<template>
  <div class="board1">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <!-- <button class="cell" @click="this.gameStore.button_click_event(i,j)">{{ i.toString() + "|" + j.toString() }}</button> -->
        <gameCell :val="this.hitMap[i - 1][j - 1]" :loc="[i - 1, j - 1]" />
      </div>
    </div>
  </div>
  <br />
  <div class="board2">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <button class="cell" @click="this.gameStore.button_click_event(i, j)">
          {{ i.toString() + "|" + j.toString() }}
        </button>
        <!-- <q-btn square color="white" text-color="black" :label="i.toString() +'|'+  j.toString()" /> -->
      </div>
    </div>
  </div>
</template>

<style>
.cell {
  width: 30px;
  height: 30px;
}
</style>
