<template>
  <div style="position: relative">
    <div class="left-list" :style="{ width: adjustWidth }">
      <div class="list-top">
        <search-items ref="searchItem"></search-items>
      </div>
      <div class="list-middle" :class="{ show: leftListSwitch }">
        <marker-lists></marker-lists>
      </div>
      <div class="resize" @mousedown="dragStart"></div>
    </div>
  </div>
</template>

<script lang="ts">
interface DataType {
  width: number;
}
interface DomEvent extends Event {
  clientX: number;
  clientY: number;
}
import Vue from "vue";
const MarkerLists = () => import("../organisms/MarkerLists.vue");
const SearchItems = () => import("../organisms/SearchItems.vue");

export default Vue.extend({
  components: {
    MarkerLists,
    SearchItems,
  },
  data(): DataType {
    return {
      width: 345,
    };
  },
  computed: {
    adjustWidth() {
      return (this as any).smp ? "100%" : (this as any).width + "px";
    },
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
    leftListSwitch() {
      return this.$store.getters["switch/leftListSwitch"];
    },
  },
  methods: {
    limit(e: DomEvent) {
      if (e.clientX < 500 && e.clientX > 100) {
        this.$data.width = e.clientX;
      }
    },
    dragStart() {
      const that = this;
      const limit = (e: DomEvent) => {
        (that as any).limit(e);
      };
      (this as any).$root.$el.addEventListener("mousemove", limit);
      (this as any).$root.$el.addEventListener("mouseup", () => {
        (that as any).$root.$el.removeEventListener("mousemove", limit),
          { once: true };
      });
    },
  },
});
</script>

<style lang="scss" scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
  opacity: 0;
  transition: opacity 0.5s;
}
.resize {
  position: absolute;
  top: 0;
  bottom: 0;
  right: -3px;
  width: 6px;
  z-index: 5;
  cursor: ew-resize;
}
.left-list {
  width: 100%;
  position: relative;
  overflow: hidden;
}
.list-top {
  padding: 10px;
  padding-right: 5px;
  text-align: center;
  border-radius: 5px;
  color: #363636;
  background-color: white;
  position: relative;
  width: 100%;
  z-index: 2;
}
@media screen and (max-width: 500px) {
  .left-list {
    z-index: 2;
    overflow: initial;
  }
  .list-middle {
    position: absolute;
    width: 100%;
    transition: all 1s;
    top: -100vh;
  }
  .show {
    top: 57px;
  }
}
</style>