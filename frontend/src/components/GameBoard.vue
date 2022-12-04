<script></script>

<template>
  <div class="board">
    <div class="row" v-for="i in 10">
      <div v-for="j in 10">
        <button class="cell">{{ i.toString() + "|" + j.toString() }}</button>
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
