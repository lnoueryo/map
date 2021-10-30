<template>
  <div id="wrapper">
    <div id="container" :class="{ open: open }">
      <div class="main-view">
        <div>
          <left-list></left-list>
        </div>
        <div class="map-container">
          <map-view></map-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
const LeftList = () => import("~/components/spot/templates/LeftList.vue");
const MapView = () => import("~/components/spot/templates/Map.vue");
interface DataType {
  open: boolean;
  lefList: boolean;
}
export default Vue.extend({
  components: {
    LeftList,
    MapView,
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
  mounted() {
    this.$on("open", (this as any).drawer);
  },
  methods: {
    drawer() {
      //right-drawerが開いた時の処理
      (this as any).open = !(this as any).open;
    },
  },
});
</script>

<style lang="scss" scoped>
#wrapper {
  width: 100%;
  height: calc(100vh - 100px);
  position: relative;
  #container {
    width: 100%;
    position: relative;
    padding-right: 100px;
    transition: all 0.3s;
    .main-view {
      display: flex;
      overflow: hidden;
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