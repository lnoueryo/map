<template>
  <v-app dark v-resize="onResize">
    <header-bar v-if="!smp && $route.name !== 'login'"></header-bar>
    <transition name="fade">
      <nuxt :style="{paddingTop: smp ? 0 : '64px'}" />
    </transition>
        <div v-if="smp">
            <v-btn fab fixed bottom right dark small color="green" @click="$router.go(-1)">
                <v-icon>mdi-keyboard-backspace</v-icon>
            </v-btn>
        </div>
        <transition name="fade">
          <error v-if="errorDialog"></error>
        </transition>
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
        return this.$store.getters['windowSize'].x < 500;
    },
    errorDialog() {
      return this.$store.getters['errorDialog'];
    }
  },
  beforeCreate() {
    if (process.env.NODE_ENV === "production") {
        const parts = location.hostname.split(".");
        const subdomain = parts.shift();
        if(subdomain == 'tap-map-test') this.$axios.defaults.baseURL = 'https://tap-map-test.api.jounetsism.biz'
    }
    this.$store.dispatch('getTables')
    // this.$store.dispatch('isLogin');
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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
  transition: opacity 1s;
}
// .gm-style-iw {
//   margin-left: 10px;
// }
// .gm-style-iw > button {
//   display: none !important;
// }
</style>