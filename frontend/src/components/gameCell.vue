<script>
import { useGameStore } from "@/stores/GameStore";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
  props: ["val", "loc"],
  methods: {
    clickLog() {
      console.log(this.val);
      console.log(this.loc);
    },
  },
};
</script>

<template>
  <!-- <button :class="val" @click="this.gameStore.button_click_event(i,j)">{{ loc[0].toString() + "|" + loc[1].toString() }}</button> -->
  <button :class="val" @click="clickLog">
    {{ loc[0].toString() + "|" + loc[1].toString() }}
  </button>
</template>

<style scoped>
.hit {
  background-color: red;
  color: antiquewhite;
}
.miss {
  background-color: white;
  color: darkgrey;
}
.ocean {
  background-color: blue;
  color: darkgrey;
}
.ship {
  background-color: grey;
  color: darkgrey;
}
button {
  width: 30px;
  height: 30px;
}
</style>
