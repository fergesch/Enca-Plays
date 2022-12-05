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
  <main>
    <input v-model="gameStore.username" placeholder="Enter name" />
    <button @click="this.gameStore.create_game_event">Create Game</button>
  </main>
</template>
