<template>
  <div class="map-container">
    <div id="map" ref="map"></div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
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
  company: {name: string, id: number}
}
export default Vue.extend({
  props: ["stations"],
  computed: {
    ...mapGetters('station', [
      'combineStationsWithLines'
    ]),
    mainStation() {
      return this.$store.getters['station/particularStations'].find((station: Station) => {
        return String(station.company.id) == this.$route.params.company_id;
      })
    },
  },
  mounted() {
    let timer = setInterval(async() => {
      if(this.mainStation.name == this.$route.params.name) {
        clearInterval(timer)
        await (this as any).setMap();
      }
    },250)
  },
  methods: {
    async setMap() {
      const mainStation = JSON.parse(JSON.stringify(this.mainStation))
      delete mainStation['company']
      delete mainStation['lines']
      const mapEl = this.$refs.map;
      this.$mapConfig.makeMap(mapEl as HTMLDivElement);
      this.$mapConfig.placesService();
      this.$store.dispatch('info/spotDetail', mainStation);
      this.$store.dispatch("info/getAroundSpot", { ...mainStation });
      this.$store.dispatch('info/getTwitterInfo', mainStation);
      const marker = this.$mapConfig.makeMarkerWithLabel(
        (this as any).mainStation,
        "",
        (this as any).mainStation.name
      );
      marker.addListener("click", (e: google.maps.MapMouseEvent) => {
        this.$mapConfig.map.setZoom(15);
        this.$mapConfig.map.setCenter(
          new google.maps.LatLng(
            (e.latLng as any).lat(),
            (e.latLng as any).lng()
          )
        );
      });
      this.$mapConfig.map.setZoom(15);
      this.$mapConfig.map.setCenter(
        new google.maps.LatLng(
          (this as any).mainStation.lat,
          (this as any).mainStation.lng
        )
      );
    },
  },
});
</script>

<style lang="scss" scoped>
.map-container {
  position: relative;
  width: 100%;
  max-width: 550px;
  // height: 100vh;
  // max-height: calc(var(--vh, 1vh) * 100 - 64px);
  #map {
    width: 100%;
    height: 100%;
    position: relative;
    padding-top: 75%;
    transition: all 0.5s;
  }
}
</style>