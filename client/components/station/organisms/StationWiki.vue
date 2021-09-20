<template>
  <div>
    <div ref="wiki" class="wiki">
      <div v-html="stationInfo" v-if="stationInfo"></div>
      <div v-else class="centering">
        <div>マーカーをクリックして駅情報を取得しましょう</div>
      </div>
    </div>
    <div class="url-box">
      <a :href="URL" target="_blank">{{ URL }}</a>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapGetters } from "vuex";
export default Vue.extend({
  computed: {
    ...mapGetters("station", ["selectedMarker"]),
    ...mapGetters("info", ["stationInfo"]),
    URL() {
      if (this.selectedMarker.name)
        return "https://ja.wikipedia.org/wiki/" + this.selectedMarker.name;
      return;
    },
  },
  watch: {
    stationInfo: {
      handler() {
        this.$nextTick(() => {
          const wiki = this.$refs.wiki as HTMLDivElement;
          wiki.scrollTop = 0;
          const table = wiki.getElementsByClassName(
            "infobox bordered"
          )[0] as HTMLTableElement;
          table.style.width = "";
          table.style.margin = "auto";
        });
      },
    },
  },
});
</script>

<style lang="scss" scoped>
.url-box {
  text-align: center;
  position: relative;
  bottom: 0;
  font-size: 14px;
  word-break: break-all;
  font-weight: bold;
  background-color: white;
  padding-right: 5px;
  padding-top: 3px;
}
.wiki {
  height: 100vh;
  background-color: white;
  color: black;
  overflow-x: hidden;
  overflow-y: scroll;
  max-height: calc(var(--vh, 1vh) * 100 - 70px);
}
.centering {
  display: flex;
  align-items: center;
  height: 100%;
}
</style>