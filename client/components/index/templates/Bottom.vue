<template>
  <div>
    <half-modal :show="ready" @hide="ready = false">
      <station-wiki></station-wiki>
    </half-modal>
    <div class="lazy" v-if="this.$store.getters['info/searching']">
      <v-card color="orange" dark height="40">
        <v-card-text style="height: 30px; padding: 5px 10px">
          Please stand by
          <v-progress-linear
            indeterminate
            color="white"
            class="mb-0"
          ></v-progress-linear>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<script>
const HalfModal = () => import("../../global/HalfModal.vue");
const StationWiki = () => import("../organisms/StationWiki.vue");
export default {
  components: {
    HalfModal,
    StationWiki,
  },
  data() {
    return {
      ready: false,
    };
  },
  computed: {
    stationInfo() {
      return this.$store.getters["info/stationInfo"];
    },
  },
  watch: {
    stationInfo: {
      handler() {
        this.ready = true;
      },
    },
  },
};
</script>

<style lang="scss" scoped>
.lazy {
  position: absolute;
  bottom: 7%;
  left: 50%;
  transform: translateY(-50%) translateX(-50%);
  width: 100%;
  padding: 0 10px;
  max-width: 300px;
  z-index: 15;
}
</style>