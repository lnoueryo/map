<template>
  <div id="wrapper">
    <div id="container" :class="{ open: open }">
      <div class="main-view">
        <div>
          <left-list></left-list>
        </div>
        <div class="map-container">
          <stations-map></stations-map>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
const LeftList = () => import("~/components/station/templates/LeftList.vue");
const StationsMap = () => import("~/components/station/templates/StationsMap.vue");
interface DataType {
  open: boolean;
  lefList: boolean;
}
export default Vue.extend({
  components: {
    LeftList,
    StationsMap,
  },
  data(): DataType {
    return {
      open: false,
      lefList: false,
    };
  },
  computed: {
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
  },
  created() {
    this.$store.dispatch('station/params', this.$route);
    this.$store.dispatch('station/getStations', this.$route.params);
    this.$store.dispatch('station/getLines', this.$route.params);
  }
});
</script>

<style lang="scss" scoped>
#wrapper {
  width: 100%;
  height: 100%;
  max-height: calc(100vh);
  overflow: hidden;
  position: relative;
  #container {
    width: 100%;
    position: relative;
    padding-right: 100px;
    transition: all 0.3s;
    .main-view {
      display: flex;
      overflow: hidden;
      max-height: calc(100%-200px);
      .map-container {
        position: relative;
        width: 100%;
      }
    }
    @media screen and (max-width: 500px) {
      .main-view {
        //left-listを上げて、map-viewを下げる
        display: block;
      }
    }
  }
  #container.open {
    padding-right: 256px;
    transition: all 0.3s;
  }
  @media screen and (max-width: 500px) {
    #container {
      padding-right: 0;
    }
    #container.open {
      padding-right: 0;
      transition: all 0.3s;
    }
  }
}
</style>