<template>
  <div>
    <div class="list-bottom">
      <div class="d-flex my-2 px-3" style="font-size: 14px">
        <toggle-switch
          class="mr-3 w50"
          v-model="chartSwitch"
          id="chartSwitch"
          background-color="#ff9800"
          >グラフ</toggle-switch
        >
        <toggle-switch
          class="w50"
          v-model="dotSwitch"
          id="dotSwitch"
          background-color="#ff9800"
          >ドット</toggle-switch
        >
      </div>
      <div class="d-flex my-2 px-3" style="font-size: 14px">
        <toggle-switch
          class="mr-3 w50"
          v-model="markerSwitch"
          id="markerSwitch"
          background-color="#ff9800"
          >マーカー</toggle-switch
        >
        <toggle-switch
          class="w50"
          v-model="lineSwitch"
          id="lineSwitch"
          background-color="#ff9800"
          >ライン</toggle-switch
        >
      </div>
      <v-btn color="red" outlined block @click="$parent.onClickCircleButton"
        >閉じる</v-btn
      >
    </div>
  </div>
</template>

<script>
import Vue from "vue";
const ToggleSwitch = () => import("../../global/ToggleSwitch.vue");
export default Vue.extend({
  components: {
    ToggleSwitch,
  },
  computed: {
    markerSwitch: {
      get() {
        return this.$store.getters["switch/markerSwitch"];
      },
      set(value) {
        this.$store.dispatch("switch/changeMarkerSwitch", value);
      },
    },
    lineSwitch: {
      get() {
        return this.$store.getters["switch/lineSwitch"];
      },
      set(value) {
        this.$store.dispatch("switch/changeLineSwitch", value);
      },
    },
    chartSwitch: {
      get() {
        return this.$store.getters["switch/chartSwitch"];
      },
      set(value) {
        this.$store.dispatch("switch/changeChartSwitch", value);
      },
    },
    dotSwitch: {
      get() {
        return this.$store.getters["switch/dotSwitch"];
      },
      set(value) {
        this.$store.dispatch("switch/changeDotSwitch", value);
      },
    },
  },
  methods: {
    onClickChart() {
      this.$refs.chartInput.click();
    },
  },
});
</script>

<style lang="scss" scoped>
.list-bottom {
  position: absolute;
  bottom: 0;
  right: 0;
  left: 0;
  z-index: -1;
  margin: auto;
}
.w50 {
  width: 50%;
}
</style>