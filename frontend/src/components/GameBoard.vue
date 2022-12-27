<script>
import { useGameStore } from "@/stores/GameStore";
import gameCell from "./gameCell.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  name: "Board",
  methods: {
        endSubPhase() {
            
        },
        resetSubPhase(){

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
        <gameCell :val="this.gameStore.oppBoard[i - 1][j - 1]" :loc="[i - 1, j - 1]" board="oppBoard" />
        <!-- <gameCell :val="this.hitMap[i - 1][j - 1]" :loc="[i - 1, j - 1]" board="oppBoard"/> -->
      </div>
    </div>
  </div>
  <br />
  <div class="myBoard">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <gameCell :val="this.gameStore.myBoard[i - 1][j - 1]" :loc="[i - 1, j - 1]" board="myBoard" />
      </div>
    </div>
  </div>
  <!-- make a button that shows up in the SHIP Confirm subphase that sets shipPosition and moves to next ship -->
  <button v-if="this.gameStore.gameSubPhase.includes('Confirm')" @click="endSubPhase">Confirm Ship</button>
  <button v-if="this.gameStore.gameSubPhase.includes('Confirm')" @click="resetSubPhase">Reset Current Ship</button>
  <button v-if="this.gameStore.gameSubPhase == 'Submit Ships'" @click="this.gameStore.submit_ships()">Submit Ships</button>
</template>

<style>
.cell {
  width: 30px;
  height: 30px;
}
</style>
