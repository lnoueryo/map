<template>
  <v-app dark v-resize="onResize">
    <header-bar v-if="!smp"></header-bar>
    <nuxt :style="{paddingTop: smp ? 0 : '64px'}" />
    <!-- <v-main>
            <v-container>
                <nuxt />
            </v-container>
        </v-main> -->
    <!-- <v-footer :absolute="!fixed" app>
        <span>&copy; {{ new Date().getFullYear() }}</span>
        </v-footer> -->
        <div v-if="smp">
            <v-btn fab fixed bottom right dark small color="green" @click="$router.go(-1)">
                <v-icon>mdi-keyboard-backspace</v-icon>
            </v-btn>
        </div>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import HeaderBar from "../components/global/HeaderBar.vue";
import { setHeight, invalidHover } from "../utils/smp";

export default Vue.extend({
  components: {
    HeaderBar,
  },
  data() {
    return {
      windowSize: { x: 0, y: 0 },
    };
  },
  computed: {
    smp() {
        return this.$store.getters['windowSize'].x < 500
    },
  },
  beforeCreate() {
    if (process.env.NODE_ENV === "production") {
      if (window.location.hostname === "map-ai7ganlifq-an.a.run.app") {
        this.$axios.defaults.baseURL = "/";
      }
    }
    this.$store.dispatch("isAuth", this.$route.name);
  },
  mounted() {
    this.onResize();
  },
  methods: {
    onResize() {
      this.$store.dispatch("windowSize", {
        x: window.innerWidth,
        y: window.innerHeight,
      });
      setHeight();
      invalidHover();
    },
  },
});
</script>

<style lang="scss">
.labels {
  color: #ffffff;
  background: #005bb5;
  font-size: 8px;
  text-align: center;
  padding: 2px 10px;
  border-radius: 8px;
}
// .gm-style-iw {
//   margin-left: 10px;
// }
// .gm-style-iw > button {
//   display: none !important;
// }
</style>