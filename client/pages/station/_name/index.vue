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
        <div ref="wiki" class="wiki" :style="{maxWidth: stationWikiInfo ? '330px' : '0', transition: stationWikiInfo ? 'all 1.5s' : 'all .5s'}" v-if="!smp">
          <div v-html="stationWikiInfo"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
const LeftList = () => import("~/components/station/templates/LeftList.vue");
const MapView = () => import("~/components/station/templates/Map.vue");
const HalfModal = () => import("~/components/global/HalfModal.vue");
interface AroundStationInfo { "Name": string, "Uid": string, "Category": string, "Label": string, "Combined": string}
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string, geohash: string, company: Company }
interface Company { id: number, name: string, address: string, founded: string, lines: Line[] };
interface Line { id: number, company_id: number, name: string, polygon: Polygon, color: string, stations: Station[] };
interface Polygon { lat: number, lng: number }[];
export default Vue.extend({
  data() {
    return {
      open: false,
      dialog: false,
      dialogPhoto: null,
      copyStationInfo: null,
      wikiReady: false
    }
  },
  components: {
    MapView,
    LeftList,
    HalfModal
  },
  beforeCreate() {
    this.$store.dispatch('station/params', this.$route.params);
  },
  computed: {
    stationInfo() {
      return this.$store.getters['station/stationInfo'];
    },
    stationWikiInfo() {
      return this.$store.getters['info/stationInfo'];
    },
    placesData() {
      return this.$store.getters['info/spotDetail'];
    },
    nearestStations() {
      const nearestStations = this.$store.getters['station/combineStationsWithLines'].filter((station: Station) => {
        return station.geohash.includes((this as any).stationInfo.geohash.slice(0, -1));
      });
      return nearestStations.map((station: Station) => {
        const company = this.$store.getters['station/companies'].find((company: Company) => {
          return company.id == station.company_id;
        })
        station['company'] = company;
        return station;
      })
    },
    aroundStationInfo() {
      return this.$store.getters['info/aroundStationInfo'];
    },
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
  },
  methods: {
    roundHalf(num: number) {
        return Math.round(num * 2) / 2;
    },
    changeTime(time: string) {
      let date = new Date(time);
      const year = date.getFullYear();
      const month = ("0" + (date.getMonth() + 1)).slice(-2);
      const day = ("0" + date.getDate()).slice(-2);
      const hours = ("0" + date.getHours()).slice(-2);
      const minutes = ("0" + date.getMinutes()).slice(-2);
      const changedDate = `${year}-${month}-${day} ${hours}:${minutes}`;
      return changedDate;
    },
  }
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
.wiki {
  height: 100vh;
  background-color: white;
  color: black;
  overflow-x: hidden;
  overflow-y: scroll;
  max-height: calc(var(--vh, 1vh) * 100 - 65px);
  padding: 0 5px;
}
</style>