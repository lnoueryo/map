<template>
  <div>
    <transition name="fade">
      <div
        class="middle-list"
        :style="
          leftListSwitch
            ? { bottom: '100vh', transition: 'all 1.8s' }
            : { bottom: '0', transition: 'all .8s' }
        "
      >
        <simple-lists
          :items="$store.getters['spot/boundsFilter'](prefectures)"
          @item="prefecture = { ...prefecture, ...$event }"
          v-if="!$route.query.prefecture_id"
          >都道府県を選択してください</simple-lists
        >
        <simple-lists
          :items="$store.getters['spot/boundsFilter'](cities)"
          @item="city = { ...city, ...$event }"
          v-if="$route.query.prefecture_id && !$route.query.city_code"
        >
        {{filterPrefectures.name}}
        </simple-lists>
        <simple-lists
          :items="$store.getters['spot/boundsFilter'](spots)"
          @item="spot = { ...spot, ...$event }"
          v-if="$route.query.prefecture_id && $route.query.city_code"
        >
        <div @click="moveToCity(filterPrefectures)">{{filterPrefectures.name}}</div>
        </simple-lists>
      </div>
    </transition>
  </div>
</template>


<script lang="ts">
interface Prefecture {
  id: string;
  name: string;
  wiki: string;
  lat: number;
  lng: number;
  cities: City[];
}
interface City {
  prefecture_id: string
  name: string;
  wiki: string;
  id: string;
  lat: string;
  lng: string;
  city: string;
  spots: Spot[];
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
interface DataType {
  listNum: number;
  prefecture: Prefecture | null;
  city: City | null;
  spot: Spot | null;
  wikiReady: boolean;
  placesReady: boolean;
  currentWikiData: string;
}
import Vue from "vue";
const SimpleLists = () => import("../../global/SimpleLists.vue");
import { mapGetters } from "vuex";
export default Vue.extend({
  components: {
    SimpleLists,
  },
  data(): DataType {
    return {
      listNum: 0,
      prefecture: null,
      city: null,
      spot: null,
      wikiReady: false,
      placesReady: false,
      currentWikiData: "",
    };
  },
  computed: {
    ...mapGetters("spot", [
      "filterPrefectures",
    ]),
    ...mapGetters("switch", [
      "leftListSwitch",
    ]),
    ...mapGetters("info", ["cityWikiInfo", "spotDetail"]),
    prefectures() {
      return this.filterPrefectures || [];
    },
    cities() {
      return this.filterPrefectures?.cities || [];
    },
    spots() {
      return this.filterPrefectures?.spots || [];
    },
  },
  watch: {
    prefecture(v) {
      const query = { ...this.$route.query, ...{ prefecture_id: v.id } };
      this.$router.push({name: 'spot', query: query});
    },
    city(v) {
      const query = { ...this.$route.query, ...{ city_code: v.id } };
      this.$router.push({name: 'spot', query: query});
    },
    spot(v) {
      this.$router.push({name: 'spot-detail-prefecture_id-city_code-id', params: {prefecture_id: v.prefecture_id, city_code: v.city_code, id: v.id}})
    }
  },
  methods: {
    back() {
      const query = { ...{}, ...this.$route.query } as any;
      const queryArray = Object.keys(this.$route.query);
      if (queryArray.length !== 0) delete query[queryArray.slice(-1)[0]];
      delete query[queryArray.slice(-1)[0]];
      this.$router.push({ query: query });
    },
    getWiki(obj: City | Prefecture) {
      (this.$parent.$refs.modals as any).getWiki(obj);
    },
    moveToCity(city: City) {
      this.$router.push({'name': 'prefecture-prefecture_id-city_code', params: {prefecture_id: city.prefecture_id, city_code: city.id}})
    }
    // hideWiki() {
    //     (this as any).wikiReady = false;
    // },
    // hidePlaces() {
    //     (this as any).placesReady = false;
    // }
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
}
.middle-list {
  overflow-y: scroll;
  overflow-x: hidden;
  height: 100vh;
  max-height: calc(var(--vh, 1vh) * 100 - 164px);
  .company-name {
    text-align: center;
    border-radius: 5px;
    color: white;
    background-color: #363636;
    width: 100%;
    display: block;
    padding: 10px;
    transition: all 0.5s;
    cursor: pointer;
  }
  .company-name:hover {
    opacity: 0.7;
    transition: all 0.5s;
  }
  .company-name:active {
    opacity: 0.9;
    transition: all 0.5s;
  }
  .line-name {
    text-align: center;
    border-radius: 5px;
    color: white;
    width: 100%;
    display: block;
    padding: 10px;
    transition: all 0.5s;
    cursor: pointer;
  }
  .line-name:hover {
    opacity: 0.7;
    transition: all 0.5s;
  }
  .line-name:active {
    opacity: 0.9;
  }
  .list-move {
    transition: transform 1s;
  }
  .list-enter {
    opacity: 0;
    transform: translateX(256px);
  }
  .list-enter-active {
    transition: all 1s;
  }
  .list-leave-active {
    transition: all 1s;
    position: absolute;
  }
  .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
    opacity: 0;
    transform: translateX(256px);
  }
}
@media screen and (max-width: 500px) {
  .middle-list {
    //リストを上から半分出す
    height: initial;
    max-height: calc(50vh - 55px);
  }
}
</style>