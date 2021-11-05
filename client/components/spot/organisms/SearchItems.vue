<template>
  <div>
    <div class="d-flex">
      <search-bar
        ref="searchBar"
        placeholder="観光地を検索"
        @select="select(filteredsearchResult[0])"
        @searchWord="searchTown($event)"
      >
        <div
          class="menu"
          v-if="searchResult.length !== 0"
          style="background-color: white"
        >
          <div
            @mouseup.stop.prevent="select(searchResult)"
            v-for="(searchResult, i) in filteredsearchResult"
            :key="i"
            class="list"
          >
            <span>{{ searchResult.address }}</span>
          </div>
        </div>
      </search-bar>
      <div>
        <v-btn
          class="ml-1"
          icon
          color="indigo"
          @click="$parent.$data.width = 345"
          v-if="pc"
        >
          <v-icon>mdi-arrow-collapse-horizontal</v-icon>
        </v-btn>
        <v-btn
          class="ml-1"
          icon
          color="orange"
          @click="changeLeftListSwitch = !changeLeftListSwitch"
          :style="
            changeLeftListSwitch
              ? { transform: 'rotateX(0deg)' }
              : { transform: 'rotateX(180deg)' }
          "
          v-if="smp"
        >
          <v-icon>mdi-chevron-down</v-icon>
        </v-btn>
      </div>
    </div>
    <div style="padding: 10px" v-if="pc">
      <span>現在の表示件数</span>
      <b>{{ countMarkers }}</b>
      <span>件</span>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import { mapGetters } from "vuex";
const SearchBar = () => import("../../global/SearchBar.vue");
const ToggleSwitch = () => import("../../global/ToggleSwitch.vue");

interface DataType {
  countMarkers: number;
  timer: Node | null;
}
interface Station {
  company_name: string;
  id: number;
  line_name: string;
  order: number;
  pref_name: string;
  lat: number;
  lng: number;
  name: string;
}
interface Spot {
  id: number;
  name: string;
  place_id: string;
  address: string;
  lat: number;
  lng: number;
  prefecture_id: string;
  city_code: string;
  geohash: string;
}
interface Town {
  name: string;
  address: string;
  prefecture_id: string;
  lat: string;
  lng: string;
  city_code: string;
}

export default Vue.extend({
  components: {
    SearchBar,
    ToggleSwitch,
  },
  data(): DataType {
    return {
      countMarkers: 0,
      timer: null,
    };
  },
  computed: {
    ...mapGetters("spot", ["showNumberOfMarkers", "searchResult"]),
    changeLeftListSwitch: {
      get() {
        return this.$store.getters["switch/leftListSwitch"];
      },
      set(newValue) {
        this.$store.dispatch("switch/changeLeftListSwitch", newValue);
      },
    },
    pc() {
      return this.$store.getters.windowSize.x > 500;
    },
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
    filteredsearchResult() {
      return this.searchResult.filter((_: any, index: number) => {
        return index < 5;
      });
    },
  },
  watch: {
    showNumberOfMarkers(newValue, OldValue) {
      //vuexから表示されている数の変化を検知
      (this as any).count(newValue, OldValue);
    },
  },
  methods: {
    select(town: Town) {
      // this.$store.dispatch('spot/getPrefectures')
      console.log(town)
      this.$router.push({
        name: "spot",
        query: { prefecture_id: town.prefecture_id, city_code: town.city_code, lat: town.lat, lng: town.lng},
      });
      this.$refs.searchBar.blur = false;
    },
    count(newValue: number, OldValue: number): void {
      const DURATION = 600;
      const from = OldValue;
      const to = newValue;
      const startTime = Date.now();
      let timer = setInterval(() => {
        const elapsedTime = Date.now() - startTime;
        const progress = elapsedTime / DURATION;

        if (progress < 1) {
          this.$data.countMarkers = Math.floor(from + progress * (to - from));
        } else {
          clearInterval(timer);
          this.$data.countMarkers = to;
        }
      }, 1);
    },
    searchTown(word: string) {
      if ((this as any).timer) clearTimeout((this as any).timer);
      (this as any).timer = setTimeout(
        () => this.$store.dispatch("spot/searchTown", word),
        750
      );
    },
  },
});
</script>

<style lang="scss" scoped>
.list {
  background-color: orange;
  text-align: left;
  padding: 8px 15px;
  cursor: pointer;
  color: rgb(99, 61, 61);
  transition: all 0.5s;
  // border-color: black;
  // outline: 0;
  // box-shadow: inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(102, 175, 233, .6);
}
.list:hover {
  opacity: 0.7;
  text-align: left;
  padding: 8px 15px;
  transition: all 0.5s;
}
.list:active {
  color: rgb(0, 0, 0);
  opacity: 0.8;
  transition: all 0.5s;
}
.w50 {
  width: 50%;
}
</style>