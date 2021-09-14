<template>
  <div>
    <nav class="top-bar">
      <search-bar ref="searchBar" placeholder="駅を検索" v-model="searchWord">
      </search-bar>
    </nav>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import SearchBar from "../../global/SearchBar.vue";
import { mapGetters } from "vuex";
interface Station {
  name: string;
  id: number;
  line_id: number;
  order: number;
  prefecture: string;
  lat: number;
  lng: number;
  company_id: number;
  city_code: string;
}
export default Vue.extend({
  components: {
    SearchBar,
  },
  data() {
    return {
      seachItems: { count: false, button: false },
    };
  },
  computed: {
    ...mapGetters("home", ["showNumberOfMarkers"]),
    searchWord: {
      get() {
        return this.$store.getters["home/searchWord"];
      },
      set(newValue) {
        this.$store.dispatch("home/searchWord", newValue);
      },
    },
  },
  methods: {
    onClickChangeList() {
      this.$store.dispatch("switch/changeList");
    },
    select(searchStation: Station) {
      const searchBar = this.$refs.searchBar as any;
      // const searchBar = this.$refs.searchBar as InstanceType<typeof SearchBar>;
      searchBar.$data.blur = false;
      const input = searchBar.$refs.input as HTMLInputElement;
      input.blur();
      if (searchStation) {
        this.$store.dispatch("home/selectMarker", searchStation);
        this.$store
          .dispatch("info/getStationInfo", { name: searchStation.name })
          .then(() => {
            this.$store.commit("info/searching", false);
          });
      } else {
        alert("見つかりませんでした");
      }
    },
  },
});
</script>

<style lang="scss" scoped>
.top-bar {
  position: fixed;
  bottom: 0;
  right: 0;
  left: 0;
  top: 64px;
  height: 50px;
  background-color: #ffffff;
  // background-color: #272727;
  display: flex;
  align-items: center;
  z-index: 2;
}
.list {
  background-color: orange;
  text-align: left;
  padding: 8px 15px;
  z-index: 10;
}
</style>