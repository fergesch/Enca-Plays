<script>
import { useGameStore } from "@/stores/GameStore";


export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  name: 'Board',
  components: {
  },

}
</script> 

<template>
  <div class="board">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <button class="cell" @click="this.gameStore.button_click_event(i,j)">{{ i.toString() + "|" + j.toString() }}</button>
        <!-- <q-btn square color="white" text-color="black" :label="i.toString() +'|'+  j.toString()" /> -->
      </div>
    </div>
  </div>
</template>

<style>
.cell {
  width: 50px;
  height: 50px;
}
</style>
