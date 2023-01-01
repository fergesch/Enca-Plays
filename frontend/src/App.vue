<script>
import { RouterLink, RouterView } from "vue-router";

import { useGameStore } from "@/stores/GameStore";
import { io } from "socket.io-client";

import modalPopup from "@/components/modalPopup.vue"

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },

  components: {
    modalPopup,
  },

  mounted() {
    this.gameStore.socketObj = io(import.meta.env.VITE_API_ENDPOINT, {
      transports: ["websocket", "polling", "flashsocket"],
    });

    // Should try to move the below on commands into another file
    this.gameStore.socketObj.on("after connect", (data) => {
      console.log(data);
    });

    this.gameStore.socketObj.on("joined", (data) => {
      console.log(data);
      this.gameStore.recieve_room(data["room"]);
      this.$router.push("/game");
    });

    this.gameStore.socketObj.on("modal_event", (data) => {
      this.gameStore.modalMessage = data["message"];
      this.gameStore.showModal = true;
    });
  },
  beforeUnmount() {
    this.gameStore.socketObj.disconnect();
  },
};
</script>

<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="@/assets/fergesch_logo.svg"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/game">Game</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
  <modalPopup
      :show="gameStore.showModal"
      :message="gameStore.modalMessage"
      :blocking="gameStore.modalBlocking"
      @close="gameStore.showModal = false"
    ></modalPopup>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
