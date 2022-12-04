<script>
import SocketioService from '@/services/socket.js';


export default {
  name: 'Board',
  components: {
  },
  created() {
    SocketioService.setupSocketConnection();
  },
  beforeUnmount() {
    SocketioService.disconnect();
  },
  methods: {
    buttonClickEvent(i, j) { SocketioService.button_click_event(i, j)}
  }

}
</script> 

<template>
  <div class="board">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <button class="cell" @click="buttonClickEvent(i,j)">{{ i.toString() + "|" + j.toString() }}</button>
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
