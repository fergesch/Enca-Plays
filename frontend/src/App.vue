<script>
import { RouterLink, RouterView } from "vue-router";

import { useGameStore } from "@/stores/GameStore";
import { io } from "socket.io-client";

import ModalPopup from "@/components/ModalPopup.vue";

export default {
  setup() {
    const gameStore = useGameStore();
    return { gameStore };
  },

  components: {
    ModalPopup,
    RouterLink,
    RouterView,
  },

  mounted() {
    this.gameStore.socketObj = io(import.meta.env.VITE_API_ENDPOINT, {
      transports: ["websocket", "polling", "flashsocket"],
    });


    this.gameStore.socketObj.on("joined", (data) => {
      this.gameStore.recieve_room(data["room"]);
      this.$router.push("/game");
    });

    this.gameStore.socketObj.on("players_ready", (data) => {
      this.gameStore.modal["show"] = false;
      this.gameStore["phase"] = data["phase"];
    });

    this.gameStore.socketObj.on("return_missile", (data) => {
      this.gameStore["username"] == data["username"]
        ? this.gameStore["myMissiles"].push(data["loc"])
        : this.gameStore["oppMissiles"].push(data["loc"]);
      this.gameStore["phase"] = data["phase"];
    });

    this.gameStore.socketObj.on("modal_event", (data) => {
      this.gameStore.modal["message"] = data["message"];
      this.gameStore.modal["show"] = true;
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
  </header>

  <RouterView />
  <ModalPopup
    :show="gameStore.modal['show']"
    :message="gameStore.modal['message']"
    :blocking="gameStore.modal['blocking']"
    @close="gameStore.modal['show'] = false"
  ></ModalPopup>
</template>

<style scoped>

.logo {
  display: block;
  margin: 0 auto 2rem;
}

header {
  line-height: 1.5;
  max-height: 100vh;
  /* display: flex; */
  /* place-items: center; */
  padding-right: calc(var(--section-gap) / 2);
}


</style>
