<template>
  <div class="map-container">
    <div id="map" ref="map"></div>
  </div>
</template>

<script lang="ts">
const gh = require("ngeohash");
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
  company: any;
  lines: any;
  geohash: string;
}
interface Line {
  id: number;
  company_id: number;
  name: string;
  polygon: google.maps.LatLng[];
  color: string;
  stations: Station[];
}
interface Polygon {
  lat: number;
  lng: number;
}
[];
interface Params { prefecture_id: string, city_code: string, id: number, name: string, company_id: string }
interface Query { company_id: string, line_id: string }
interface DataType {
  station: Station | null;
  markers: google.maps.Marker[][]
  otherStaionsMarkers: google.maps.Marker[]
  polylines: google.maps.Polyline[]
}
export default Vue.extend({
  data(): DataType {
    return {
      station: null,
      markers: [],
      otherStaionsMarkers: [],
      polylines: [],
    };
  },
  computed: {
    ...mapGetters("station", ["stationInfo", "filteredStation"]),
    filterStation() {
      (this as any).station = JSON.parse(
        JSON.stringify(this.filteredStation[0])
      );
      delete (this as any).station["lines"];
      return this.filteredStation;
    },
    nearestSpots() {
      const neighbors = (this as any).filterStation.forEach(
        (station: Station) => {
          gh.neighbors(station.geohash);
        }
      );
      const uniqueNeighbors = Array.from(new Set(neighbors.flat()));
      return uniqueNeighbors;
    },
  },
  watch: {
    $route: {
      async handler(v) {
        await this.$store.dispatch("station/query", v.query);
        (this as any).makeMarkers();
        (this as any).makePolylines();
        this.$mapConfig.resetMarkers((this as any).markers);
        this.$mapConfig.resetMarkers([(this as any).otherStaionsMarkers]);
        (this as any).makeOtherStaionsMarkers(v.query, v.params)
      },
      immediate: true,
    },
  },
  async mounted() {
    this.$store.dispatch("station/query", this.$route.query);
    await (this as any).setMap();
    this.$mapConfig.map.setZoom(15)
    this.$mapConfig.map.panTo(
      new google.maps.LatLng(
        (this as any).filterStation[0].lat,
        (this as any).filterStation[0].lng
      )
    );
  },
  methods: {
    async setMap() {
      const mapEl = this.$refs.map;
      this.$mapConfig.makeMap(mapEl as HTMLDivElement);
      this.$mapConfig.placesService();
      (this as any).makeMarkers();
      (this as any).makePolylines();
      this.$store.dispatch("info/getStationInfo", (this as any).station);
    },
    async makeMarkers() {
      (this as any).markers = await this.$mapConfig.makeMarkers(
        [{ stations: this.filterStation }],
        "stations",
        (this as any).onClickMarker
      );
      // this.$mapConfig.map.setZoom(15);
    },
    makeOtherStaionsMarkers(query: Query, params: Params) {
      let lines
      if('line_id' in query) {
        const lineIds = query.line_id.split(',')
        lines = [].concat(...this.filteredStation[0].lines.map((line: Line) => {
          if(lineIds.includes(String(line.id))) return line;
        }));
      } else {
        lines = [].concat(...this.filteredStation.map((station: Station) => station.lines));
      }
      const stations = lines.map((line: Line) => {
          return line.stations;
      })
      const otherStations = [].concat(...(stations as any));
      let map = new Map(otherStations.map((otherStation: Station) => [otherStation.id, otherStation]));
      const uniqueOtherStations = Array.from(map.values());
      (this as any).otherStaionsMarkers = uniqueOtherStations.map((station: Station) => {
        if(params.name !== station.name) {
          const marker = this.$mapConfig.makeMarkerWithLabel(station, '', station.name);
          marker.addListener("click", (e: google.maps.MapMouseEvent) => {
            this.$router.push({name: 'station-name', params: {name: station.name}})
          })
          return marker;
        }
      })
    },
    async makePolylines() {
      this.$mapConfig.resetPolyline((this as any).polylines);
      (this as any).polylines = (this as any).filterStation.map((station: Station) => {
        const polylines = station.lines.map((line: Line) => {
          const polyline = this.$mapConfig.makePolyline(line);
          polyline.addListener("click", () => {
            if ('line_id' in this.$route.query) {
              this.$router.push({
                name: 'station-name',
                params: { name: station.name },
                query: { company_id: String(station.company_id) },
              });
            } else {
              this.$router.push({
                name: 'station-name',
                params: { name: station.name },
                query: {
                  company_id: String(station.company_id),
                  line_id: String(line.id),
                },
              });
            }
          });
          return polyline;
        });
        return polylines;
      });
      (this as any).polylines = Array.from(new Set((this as any).polylines.flat()));
      // this.polylines = await this.$mapConfig.makePolyline();
    },
    onClickMarker(marker: google.maps.Marker, station: Station) {
      marker.addListener("click", (e: google.maps.MapMouseEvent) => {
        if ('company_id' in this.$route.query) {
          this.$router.push({
            name: 'station-name',
            params: { name: station.name },
          });
        } else {
          this.$router.push({
            name: 'station-name',
            params: { name: station.name },
            query: { company_id: String(station.company_id) },
          });
        }
      });
    },
  },
});
</script>

<style lang="scss" scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100vh;
  max-height: calc(var(--vh, 1vh) * 100 - 65px);
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
      max-height: calc(var(--vh, 1vh) * 100 - 120px);
    }
  }
}
</style>