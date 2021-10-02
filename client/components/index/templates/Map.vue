<template>
  <div class="map-container">
    <map-top class="map-top"></map-top>
    <div id="map" ref="map" :class="{ 'show-line': chartSwitch }"></div>
    <div class="dot" v-if="dotSwitch"></div>
  </div>
</template>

<script lang="ts">
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
interface DataType {
  markers: { [key: string]: google.maps.Marker[][] };
  polygons: google.maps.Polygon[][];
  timer: null | NodeJS.Timer;
}
// interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Prefecture {
  id: string;
  name: string;
  lat: number;
  lng: number;
  cities: City[];
}

interface City {
  city_code: string;
  province: string;
  lat: string;
  lng: string;
  city: string;
  spots: Spot;
}
interface Coordinate {
  lat: number;
  lng: number;
}
interface Spot {
  name: string;
  place_id: string;
  address: string;
  lat: string;
  lng: string;
  prefecture_id: string;
  city_code: string;
  id: number;
}

export default Vue.extend({
  components: {
    MapTop,
  },
  data(): DataType {
    return {
      markers: {},
      polygons: [],
      timer: null,
    };
  },
  computed: {
    ...mapGetters("home", [
      "fields",
      "prefectures",
      "selectedMarker",
      "selectedCityItems",
    ]),
    ...mapGetters("switch", [
      "markerSwitches",
      "markerSwitch",
      "lineSwitch",
      "chartSwitch",
      "dotSwitch",
    ]),
  },
  watch: {
    $route(to, from) {
      if ("click" in to.query) {
        const bounds = sessionStorage.getItem("tokyo-map") as string;
        this.$mapConfig.focusMarker(JSON.parse(bounds), 11);
      }
      this.$store.dispatch('home/query', to.query)
      this.checkQuery();
    },
  },
  beforeCreate() {
    this.$store.dispatch('home/query', this.$route.query)
    this.$store.dispatch("switch/makeSwitches");
  },
  created() {
    this.fields.forEach((field: string) => {
      this.markers[field] = [];
    });
  },
  async mounted() {
    await this.setMap();
    this.checkQuery();
    let timer: NodeJS.Timer | null;

    this.$mapConfig.map.addListener("bounds_changed", () => {
      const bounds = this.$mapConfig.currentBounds();
      const getMapCenter = this.$mapConfig.map.getCenter();
      const mapCenter = { lat: getMapCenter.lat(), lng: getMapCenter.lng() };
      const zoom = this.$mapConfig.map.getZoom();
      if (timer !== null) clearTimeout(timer);
      timer = setTimeout(() => {
        this.$store.dispatch("home/getCity", {
          mapCenter: mapCenter,
          zoom: zoom,
        });
        this.$store.dispatch("home/getCurrentBounds", bounds);
      }, 250);
    });
  },
  methods: {
    async setMap() {
      const mapEl = this.$refs.map;
      const bounds = {
        north: 37.360687,
        south: 34.030351,
        west: 137.9403931,
        east: 140.9368243,
      };
      const mapOptions = {
        zoom: 8,
        restriction: { latLngBounds: bounds, strictBounds: false },
      };
      this.$mapConfig.mapOptions(mapOptions);
      this.$mapConfig.makeMap(mapEl as HTMLElement);
      this.$mapConfig.placesService();
      // this.onClickMap()
    },
    prefectureMarkerFunction(
      marker: google.maps.Marker,
      prefecture: Prefecture
    ) {
      marker.addListener("click", async (e: google.maps.MapMouseEvent) => {
        this.$router.push(`/?prefecture_id=${prefecture.id}`);
      });
    },
    cityMarkerFunction(marker: google.maps.Marker, city: City) {
      marker.addListener("click", async (e: google.maps.MapMouseEvent) => {
        this.$router.push(
          `/?prefecture_id=${this.$route.query.prefecture_id}&city_code=${city.city_code}`
        );
      });
    },
    spotMarkerFunction(marker: google.maps.Marker, spot: Spot) {
      marker.addListener("click", (e: google.maps.MapMouseEvent) => {
        // this.$store.dispatch("info/spotDetail", spot);
        this.$router.push({name: 'detail-prefecture_id-city_code-id', params: {prefecture_id: spot.prefecture_id, city_code: spot.city_code, id: String(spot.id)}})
      });
    },
    checkQuery() {
      const query = this.$route.query;
      query?.prefecture_id && query.city_code
        ? this.selectCityMarker(query as any)
        : query?.prefecture_id
        ? this.setCityMarkers(query.prefecture_id as any)
        : this.setPrefectureMarkers();
    },
    async setPrefectureMarkers() {
      this.$mapConfig.resetAllMarkers(this.markers);
      this.markers.prefectures = await this.$mapConfig.makeMarkers(
        [{ prefectures: this.prefectures }],
        "prefectures",
        this.prefectureMarkerFunction
      );
      const mapOtions = {
        zoom: 10,
      };
      this.$mapConfig.mapOptions(mapOtions);
    },
    setCityMarkers(id: string) {
      this.$mapConfig.resetAllMarkers(this.markers);
      const prefecture = this.prefectures.find(
        (prefecture: Prefecture) => prefecture.id == id
      );
      this.markers.cities = this.$mapConfig.makeMarkers(
        [prefecture],
        "cities",
        this.cityMarkerFunction
      );
      if ("click" in this.$route.query) return;
      const zoom = 11;
      this.$mapConfig.focusMarker(prefecture, zoom);
    },
    selectCityMarker(query: { city_code: string }) {
      this.$mapConfig.resetAllMarkers(this.markers);
      const city = this.prefectures
        .reduce((a: Prefecture, b: Prefecture) => a.cities.concat(b.cities))
        .cities.find((x: City) => x.city_code == query.city_code);
      this.markers.spots = this.$mapConfig.makeMarkers(
        [city],
        "spots",
        this.spotMarkerFunction
      );
      const zoom = 14;
      this.$mapConfig.focusMarker(city, zoom);
    },
    clearTime() {
      if (this.timer) clearTimeout(this.timer);
    },
    async onClickMap(e: google.maps.MapMouseEvent) {
      this.$mapConfig.map.addListener(
        "dblclick",
        (e: google.maps.MapMouseEvent) => {
          const bounds = JSON.stringify({
            lat: (e.latLng as any).lat(),
            lng: (e.latLng as any).lng(),
          });
          sessionStorage.setItem("tokyo-map", bounds);
          const query = Object.assign({ click: null }, this.$route.query);
          const queryArray = Object.keys(this.$route.query);
          delete query[queryArray.slice(-1)[0]];
          this.$router.push({ query: query });
        }
      );
      // this.$mapConfig.map.addListener('rightclick', (e: google.maps.MapMouseEvent) => {
      //     const query = Object.assign({click: null}, this.$route.query)
      //     const queryArray = Object.keys(this.$route.query)
      //     delete query[queryArray.slice(-1)[0]]
      //     this.$router.push({query: query})
      //     const bounds = JSON.stringify({lat: e.latLng.lat(), lng: e.latLng.lng()})
      //     sessionStorage.setItem('tokyo-map', bounds);
      // })
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
  @media screen and (max-width: 500px) {
    .map-container {
      max-height: calc(var(--vh, 1vh) * 100 - 56px);
    }
  }
}
</style>