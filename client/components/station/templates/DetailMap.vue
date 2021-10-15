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
    mainStations() {
      return this.$store.getters['station/combineStationsWithLines'].filter((station: Station) => {
        return station.name == this.$route.params.name;
      })
    },
    mainStation() {
      return this.$data.mainStations.find((station: Station) => {
        return String(station.company_id) == this.$route.params.company_id;
      })
    },
  },
  async mounted() {
    await (this as any).setMap();
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
      this.$store.dispatch("info/getAroundSpotInfo", { ...mainStation });
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
      (this as any).stations.forEach((station: Station) => {
        const marker = this.$mapConfig.makeMarker(
          station,
          require("~/assets/img/station.png"),
          station.name
        );
        this.$mapConfig.createInfoWindow(
          marker,
          `${station.company.name}<br>${station.name}`
        );
        marker.addListener("click", (e: google.maps.MapMouseEvent) => {
          this.$router.push({name: 'station-name', params: {name: station.name}, query: {company_id: String(station.company.id)}})
        });
        // let infoWindow = new google.maps.InfoWindow({content: `<h3 style="color:black">${station.name}</h3>`});;
        // marker.addListener("click", (e: google.maps.MapMouseEvent) => {
        //   const tempMap = infoWindow.getMap();
        //   if (tempMap) infoWindow.close();
        //   else infoWindow.open(this.$mapConfig.map, marker);
        // });
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