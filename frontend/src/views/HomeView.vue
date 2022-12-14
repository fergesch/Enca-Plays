<script>
import { useGameStore } from "@/stores/GameStore";
import modalPopup from "@/components/modalPopup.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },

  name: 'Board',
  components: {
    modalPopup
  },
}
</script>

<template>
  <main>
    Player Name: <input v-model="gameStore.username" placeholder="Enter name" />
    <br/>
    <br/>
    <button @click="this.gameStore.create_game_event">Create Game</button>
    <br/>
    <br/>
    <input v-model="gameStore.room" placeholder="Enter room" />
    <button @click="this.gameStore.join_game_event">Join Game</button>
    <modalPopup :show="gameStore.showModal" :message="gameStore.modalMessage" @close="gameStore.showModal = false"></modalPopup>
  </main>
</template>
