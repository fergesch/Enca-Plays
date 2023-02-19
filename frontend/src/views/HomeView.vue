<script>
import { useGameStore } from "@/stores/GameStore";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },
};
</script>

<template>
  <main>
    Player Name: <input v-model="gameStore.username" placeholder="Enter name" />
    <br />
    <br />
    <button @click="this.gameStore.create_game_event">Create Game</button>
    <button @click="this.gameStore.cpu_game_event">Play vs CPU</button>
    <br />
    <br />
    <input v-model="gameStore.room" placeholder="Enter room" />
    <button @click="this.gameStore.join_game_event">Join Game</button>
  </main>
</template>
