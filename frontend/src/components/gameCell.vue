<script>
import { useGameStore } from "@/stores/GameStore";

export default {
    setup() {
        const gameStore = useGameStore();
        return { gameStore };
    },
    props: ["val", "loc", "board"],
    methods: {
        clickLog() {
            // need to handle different phases of the game using this.gameStore.gamePhase which will
            console.log(this.loc, this.val, this.board);
            // condition for gamePhase setup and board == myBoard
            if (this.board == "myBoard" && this.gameStore.gamePhase == "setup" && this.gameStore.gameSubPhase.includes("Start")) {
                this.gameStore.start_ship_event(this.loc[0], this.loc[1])
            } else if (this.board == "myBoard" && this.gameStore.gamePhase == "setup" && this.gameStore.gameSubPhase.includes("End")) {
                this.gameStore.end_ship_event(this.loc[0], this.loc[1])
            }

            // condition for gamePhase
            if (this.board == "oppBoard" && this.gameStore.gamePhase == this.gameStore.username) {
                this.gameStore.button_click_event(this.loc[0], this.loc[1])
            }
        },
    },
    data() {
        return {
            colorMap: {
                0: "ocean",
                1: "ship",
                2: "hit",
                3: "miss",
                4: "eligEnd",
                5: "shipStart",
            },
        };
    },
};
</script>

<template>
    <!-- <button :class="val" @click="this.gameStore.button_click_event(i,j)">{{ loc[0].toString() + "|" + loc[1].toString() }}</button> -->
    <button :class="colorMap[val]" @click="clickLog">
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

.eligEnd {
    background-color: yellow;
    color: black;
}

.shipStart {
    background-color: green;
    color: grey;
}

button {
    width: 30px;
    height: 30px;
}
</style>
