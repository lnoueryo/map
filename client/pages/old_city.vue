<template>
  <div id="wrapper">
    <div>
      <right-drawer></right-drawer>
    </div>
    <div id="container" :class="{ open: open }">
      <div class="main-view">
        <div>
          <left-list v-if="smp"></left-list>
        </div>
        <div class="map-container">
          <map-view></map-view>
        </div>
      </div>
    </div>
    <div>
      <top-bar v-if="!smp"></top-bar>
    </div>
    <div>
      <bottom v-if="!smp"></bottom>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
const RightDrawer = () =>
  import("~/components/old_city/templates/RightDrawer.vue");
const LeftList = () => import("~/components/old_city/templates/LeftList.vue");
const MapView = () => import("~/components/old_city/templates/Map.vue");
const TopBar = () => import("~/components/old_city/templates/TopBar.vue");
const Bottom = () => import("~/components/old_city/templates/Bottom.vue");
interface DataType {
  open: boolean;
  lefList: boolean;
}
export default Vue.extend({
  components: {
    RightDrawer,
    LeftList,
    MapView,
    TopBar,
    Bottom,
  },
  data(): DataType {
    return {
      open: false,
      lefList: false,
    };
  },
  computed: {
    smp() {
      return this.$store.getters.windowSize.x > 500;
    },
  },
  // beforeCreate(){
  //     this.$store.dispatch('switch/getCompanies', ['stations, cities']);
  // },
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