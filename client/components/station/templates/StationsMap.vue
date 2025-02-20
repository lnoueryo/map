<template>
  <div class="map-container">
    <map-top class="map-top"></map-top>
    <div id="map" ref="map"></div>
    <div class="dot"></div>
  </div>
</template>

<script lang="ts">
import MarkerClusterer from '@googlemaps/markerclustererplus';
import Vue from "vue";
import { mapGetters } from "vuex";
const MapTop = () => import("../organisms/MapTop.vue");
interface GMapWindow extends Window {
  google: any;
}
declare const window: GMapWindow;
interface Polygon {
  lat: number;
  lng: number;
}
interface Station {
  id: number;
  prefecture_id: string;
  name: string;
  lat: number;
  lng: number;
  line_id: number;
  order: number;
  company_id: number;
  city_code: string;
}
interface LinePolyline {
  lat: number;
  lng: number;
}
interface Line {
  id: number;
  company_name: string;
  name: string;
  polygon: LinePolyline[];
  color: string;
  stations: Station[];
}
interface DataType {
  markers: google.maps.Marker[][];
  polylines: google.maps.Polyline[];
  polygons: google.maps.Polygon[][];
  timer: null | NodeJS.Timer;
}
interface City {
  prefecture_id: string;
  city_code: number;
  city: string;
  polygons: Polygon[][];
}
interface Cities {
  code: string;
  province: string;
  lat: string;
  lng: string;
  city: string;
  spots: {
    name: string;
    place_id: string;
    address: string;
    lat: string;
    lng: string;
  };
}

export default Vue.extend({
  components: {
    MapTop,
  },
  data(): DataType {
    return {
      markers: [],
      polylines: [],
      polygons: [],
      timer: null,
    };
  },
  computed: {
    ...mapGetters("station", [
      'lines',
      'uniqueStations',
      'currentBounds',
      'boundsFilteredStations'
    ]),
  },
  watch: {
    currentBounds: {
      handler() {
        this.$mapConfig.boundsFilterForMarker([(this as any).markers], true)
      }
    }
  },
  async mounted() {
    await this.setMap();
    this.addMapEvent()
  },
  methods: {
    async setMap() {
      const mapEl = this.$refs.map;
      this.$mapConfig.makeMap(mapEl as HTMLElement);
      this.$mapConfig.map.setZoom(15);
    },
    addMapEvent() {
    let timer: NodeJS.Timer | null;

    this.$mapConfig.map.addListener('bounds_changed', () => {
      const bounds = this.$mapConfig.currentBounds();
      const getMapCenter = this.$mapConfig.map.getCenter();
      const mapCenter = { lat: getMapCenter.lat(), lng: getMapCenter.lng() };
      const zoom = this.$mapConfig.map.getZoom();
      if (timer !== null) clearTimeout(timer);
        timer = setTimeout(() => {
          this.$store.dispatch('station/getCity', {
            mapCenter: mapCenter,
            zoom: zoom,
          });
          this.$store.dispatch('station/getCurrentBounds', bounds);
        }, 250);
      });
      let stationTimer = setInterval(() => {
        if(this.uniqueStations.length !== 0) {
          clearInterval(stationTimer);
          this.setMarkers()
        }
      }, 250);
      let lineTimer = setInterval(() => {
        if(this.lines.length !== 0) {
          clearInterval(lineTimer);
          this.lines.forEach((line: any) => {
            const polyline = this.$mapConfig.makePolyline(line)
          });
        }
      }, 250);
    },
    async setMarkers() {
      this.markers = this.uniqueStations.map((station: Station) => {
        const marker = this.$mapConfig.makeMarkerWithLabel(station, require('~/assets/img/station.png'), station.name)
        marker.addListener("click", (e: google.maps.MapMouseEvent) => {
          this.$router.push({name: 'station-prefecture_id-name', params: {prefecture_id: '13', name: station.name}})
          // this.$router.push({name: 'station-prefectuere_id-name', params: {prefecture_id: station.prefecture_id, name: station.name}})
        })
        marker.setVisible(false)
        return marker;
      })
      const markerCluster = new MarkerClusterer(this.$mapConfig.map, (this as any).markers, {
        maxZoom: 13,
        gridSize: 90,
        imagePath:
          "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
      });
      this.$mapConfig.boundsFilterForMarker([(this as any).markers], true)
      // google.maps.event.addListener(markerCluster, 'clusterclick', function(cluster: any) {
      //     console.log(cluster.markers_);
      //     cluster.markers_.forEach(function(e){
      //         console.log(e.title);
      //     });
      // });
    },
    stationMarkerFunction(
      marker: google.maps.Marker,
      station: { name: string; company_id: number }
    ) {
      marker.addListener("click", async () => {
        this.$router.push({
          name: "station-name",
          params: { name: station.name },
          // query: {company_id: String(station.company_id)}
        });
      });
    },
    async onClickMap(e: google.maps.MapMouseEvent) {
      window.google.maps.event.clearListeners(this.$mapConfig.map, "click");
      await this.$store.dispatch("station/searchCityCode", e);
      (this as any).addClickMapListeners();
    },
    clearTime() {
      if (this.timer) clearTimeout(this.timer);
    },
  },
});
</script>

<style lang="scss" scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100vh;
  max-height: calc(var(--vh, 1vh) * 100 - 64px);
  .line-chart {
    position: absolute;
    top: 40px;
    bottom: 0;
    right: 0;
    left: 0;
    margin: auto;
  }
  .map-top {
    position: absolute;
    z-index: 1;
  }
  .dot {
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    margin: auto;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background-color: red;
    opacity: 0.4;
    transition: all 2s;
  }
  #map {
    width: 100%;
    height: 100%;
    position: relative;
    // padding-top: 56.25%;
    transition: all 0.5s;
  }
  .show-line {
    opacity: 0.4;
  }
  #overview-wrapper {
    position: absolute;
    width: 30%;
    bottom: 50px;
    left: 15px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
    #overview-container {
      position: relative;
      width: 100%;
      #overview {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
      }
    }
    #overview-container:before {
      content: "";
      display: block;
      padding-top: 56.25%;
    }
  }
}
  @media screen and(max-width: 500px) {
    .map-container {
      max-height: calc(var(--vh, 1vh) * 100 - 56px);
    }
  }
</style>