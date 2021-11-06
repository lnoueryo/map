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
  prefecture_id: string;
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
interface Params {
  prefecture_id: string;
  city_code: string;
  id: number;
  name: string;
  company_id: string;
}
interface Query {
  company_id: string;
  line_id: string;
}
interface DataType {
  station: Station | null;
  markers: google.maps.Marker[][];
  otherStaionsMarkers: google.maps.Marker[];
  polylines: google.maps.Polyline[];
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
    ...mapGetters("station", ["particularStations"]),
    filterStation() {
      if ((this as any).filteredStation !== 0) {
        (this as any).station = JSON.parse(
          JSON.stringify((this as any).filteredStation[0])
        );
        delete (this as any).station["lines"];
      }
      return (this as any).filteredStation;
    },
    nearestSpots() {
      const neighbors = (this as any).particularStations.forEach(
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
        this.$mapConfig.resetMarkers((this as any).markers);
        this.$mapConfig.resetMarkers((this as any).otherStaionsMarkers);
        (this as any).makeMarkers();
        (this as any).makePolylines();
      },
      immediate: false,
    },
  },
  created() {
    this.$store.commit('station/resetState')
    this.$store.dispatch("station/getParticularStations", this.$route.params);
    this.$store.dispatch("station/query", this.$route.query);
  },
  async mounted() {
    await (this as any).setMap();
    let timer = setInterval(() => {
      if (this.particularStations.length !== 0) {
        clearInterval(timer);
        (this as any).addMapEvent();
        (this as any).makeMarkers();
        (this as any).makePolylines();
      }
    }, 250);
  },
  methods: {
    async setMap() {
      const mapEl = this.$refs.map;
      this.$mapConfig.makeMap(mapEl as HTMLDivElement);
    },
    addMapEvent() {
      let timer: NodeJS.Timer | null;
      this.$mapConfig.map.addListener("bounds_changed", () => {
        const bounds = this.$mapConfig.currentBounds();
        const getMapCenter = this.$mapConfig.map.getCenter();
        const mapCenter = { lat: getMapCenter.lat(), lng: getMapCenter.lng() };
        const zoom = this.$mapConfig.map.getZoom();
        if (timer !== null) clearTimeout(timer);
        timer = setTimeout(() => {
          this.$store.dispatch("station/getCity", {
            mapCenter: mapCenter,
            zoom: zoom,
          });
          this.$store.dispatch("station/getCurrentBounds", bounds);
        }, 250);
      });
      this.$mapConfig.map.setZoom(15);
      this.$mapConfig.map.panTo(
        new google.maps.LatLng(
          (this as any).particularStations[0].lat,
          (this as any).particularStations[0].lng
        )
      );
    },
    async makeMarkers() {
      if ("company_id" in this.$route.query) {
        this.particularStations.forEach((mainStation: Station) => {
          if (String(mainStation.company.id) == this.$route.query.company_id) {
            const marker = this.$mapConfig.makeMarkerWithLabel(
              mainStation,
              require("~/assets/img/station.png"),
              mainStation.name
            );
            (this as any).onClickMarker(marker, mainStation);
            (this as any).markers.push(marker);
            if ("line_id" in this.$route.query) {
              mainStation.lines.forEach((line: Line) => {
                if (String(this.$route.query.line_id) == String(line.id)) {
                  line.stations.forEach((station: Station) => {
                    if (station.name !== this.particularStations[0].name) {
                      const marker = this.$mapConfig.makeMarkerWithLabel(
                        station,
                        "",
                        station.name
                      );
                      marker.addListener("click", (e: google.maps.MapMouseEvent) => {
                        this.$router.push({
                          name: "station-prefecture_id-name",
                          params: { prefecture_id: station.prefecture_id, name: station.name },
                        });
                      });
                      (this as any).otherStaionsMarkers.push(marker);
                    }
                  });
                }
              });
            } else {
              (this as any).markers.push(marker);
              mainStation.lines.forEach((line: Line) => {
                line.stations.forEach((station: Station) => {
                  if (station.name !== this.particularStations[0].name) {
                    const marker = this.$mapConfig.makeMarkerWithLabel(
                      station,
                      "",
                      station.name
                    );
                    marker.addListener("click", (e: google.maps.MapMouseEvent) => {
                      this.$router.push({
                        name: "station-prefecture_id-name",
                        params: { prefecture_id: station.prefecture_id, name: station.name },
                      });
                    });
                    (this as any).otherStaionsMarkers.push(marker);
                  }
                });
              });
            }
          }
        });
      } else {
        this.particularStations.forEach((mainStation: Station) => {
          const marker = this.$mapConfig.makeMarkerWithLabel(
            mainStation,
            require("~/assets/img/station.png"),
            mainStation.name
          );
          marker.addListener("click", (e: google.maps.MapMouseEvent) => {
            this.$router.push({
              name: "station-prefecture_id-name",
              params: { prefecture_id: mainStation.prefecture_id, name: mainStation.name },
              query: {company_id: mainStation.company.id}
            });
          });
          (this as any).markers.push(marker);
          if ("line_id" in this.$route.query) {
            mainStation.lines.forEach((line: Line) => {
              if (String(this.$route.query.line_id) == String(line.id)) {
                line.stations.forEach((station: Station) => {
                  if (station.name !== this.particularStations[0].name) {
                    const marker = this.$mapConfig.makeMarkerWithLabel(
                      station,
                      "",
                      station.name
                    );
                    marker.addListener("click", (e: google.maps.MapMouseEvent) => {
                      this.$router.push({
                        name: "station-prefecture_id-name",
                        params: { prefecture_id: station.prefecture_id, name: station.name },
                      });
                    });
                    (this as any).otherStaionsMarkers.push(marker);
                  }
                });
              }
            });
          } else {
            mainStation.lines.forEach((line: Line) => {
              line.stations.forEach((station: Station) => {
                if (station.name !== this.particularStations[0].name) {
                  const marker = this.$mapConfig.makeMarkerWithLabel(
                    station,
                    "",
                    station.name
                  );
                  marker.addListener("click", (e: google.maps.MapMouseEvent) => {
                    this.$router.push({
                      name: "station-prefecture_id-name",
                      params: { prefecture_id: station.prefecture_id, name: station.name },
                    });
                  });
                  (this as any).otherStaionsMarkers.push(marker);
                }
              });
            });
          }
        });
      }
    },
    makeOtherStaionsMarkers(query: Query, params: Params) {
      let lines;
      if ("line_id" in query) {
        const lineIds = query.line_id.split(",");
        lines = [].concat(
          ...(this as any).filteredStation[0].lines.map((line: Line) => {
            if (lineIds.includes(String(line.id))) return line;
          })
        );
      } else {
        lines = [].concat(
          ...(this as any).filteredStation.map((station: Station) => station.lines)
        );
      }
      const stations = lines.map((line: Line) => {
        return line.stations;
      });
      if (stations.length !== 0) {
        const otherStations = [].concat(...(stations as any));
        let map = new Map(
          otherStations.map((otherStation: Station) => [
            otherStation?.id,
            otherStation,
          ])
        );
        const uniqueOtherStations = Array.from(map.values());
        (this as any).otherStaionsMarkers = uniqueOtherStations.map(
          (station: Station) => {
            if (params.name !== station?.name) {
              const marker = this.$mapConfig.makeMarkerWithLabel(
                station,
                "",
                station?.name
              );
              marker.addListener("click", (e: google.maps.MapMouseEvent) => {
                this.$router.push({
                  name: "station-prefecture_id-name",
                  params: {
                    prefecture_id: station.prefecture_id,
                    name: station.name,
                  },
                });
              });
              return marker;
            }
          }
        );
      }
    },
    addPolylineEvent(polyline: google.maps.Polyline, station: Station, line: Line) {
      polyline.addListener("click", () => {
        if ("line_id" in this.$route.query) {
          this.$router.push({
            name: "station-prefecture_id-name",
            params: {
              prefecture_id: station.prefecture_id,
              name: station.name,
            },
            query: { company_id: String(station.company_id) },
          });
        } else {
          this.$router.push({
            name: "station-prefecture_id-name",
            params: {
              prefecture_id: station.prefecture_id,
              name: station.name,
            },
            query: {
              company_id: String(station.company_id),
              line_id: String(line.id),
            },
          });
        }
      });
    },
    async makePolylines() {
      this.$mapConfig.resetPolyline((this as any).polylines);
      if('company_id' in this.$route.query) {
        (this as any).polylines = (this as any).particularStations.map(
          (mainStation: Station) => {
            if(String(mainStation.company.id) == this.$route.query.company_id) {
              const polylines = mainStation.lines.map((line: Line) => {
                if ("line_id" in this.$route.query) {
                  if(String(line.id) == this.$route.query.line_id) {
                    const polyline = this.$mapConfig.makePolyline(line);
                    (this as any).addPolylineEvent(polyline, mainStation, line)
                    return polyline;
                  }
                } else {
                  const polyline = this.$mapConfig.makePolyline(line);
                  (this as any).addPolylineEvent(polyline, mainStation, line);
                  return polyline;
                }
              });
              return polylines;
            }
          }
        );
      } else {
        (this as any).polylines = (this as any).particularStations.map(
          (mainStation: Station) => {
            const polylines = mainStation.lines.map((line: Line) => {
              if ("line_id" in this.$route.query) {
                if(String(line.id) == this.$route.query.line_id) {
                const polyline = this.$mapConfig.makePolyline(line);
                (this as any).addPolylineEvent(polyline, mainStation, line)
                return polyline;
                }
              } else {
                const polyline = this.$mapConfig.makePolyline(line);
                (this as any).addPolylineEvent(polyline, mainStation, line);
                return polyline;
              }
            });
          return polylines;
          })
      }
      (this as any).polylines = Array.from(
        new Set((this as any).polylines.flat())
      ).filter((polyline) => polyline !== undefined);
    },
    onClickMarker(marker: google.maps.Marker, station: Station) {
      var latlng = new google.maps.LatLng(station.lat, station.lng);
      var infowindow = new google.maps.InfoWindow({
        content: " ",
        position: latlng,
      });
      infowindow.setContent(
        `<div>
                  <h4 style="color: black">${station.company.name}</h4>
                  <h2 style="color: black">${station.name}</h2>
                    <a id="line" style="position: relative;display: inline-block;font-weight: bold;padding: 0.25em 0.5em;text-decoration: none;color: #00BCD4;background-color: #ECECEC;transition: .4s;"><i class="fa fa-caret-right"></i> 全路線表示</a>
                    <a id="station-detail" style="position: relative;display: inline-block;font-weight: bold;padding: 0.25em 0.5em;text-decoration: none;color: #00BCD4;background-color: #ECECEC;transition: .4s;">詳細</a>
                  </div>`
      );
      infowindow.addListener("domready", () => {
        document.getElementById("line")?.addEventListener("click", () => {
          this.$router.push({
            name: "station-prefecture_id-name",
            params: { prefecture_id: station.prefecture_id, name: station.name },
          });
        });
        document
          .getElementById("station-detail")
          ?.addEventListener("click", () => {
            this.$router.push({
              name: "station-prefecture_id-name-detail-company_id",
              params: {
                prefecture_id: station.prefecture_id,
                name: station.name,
                company_id: String(this.$route.query.company_id),
              },
            });
          });
      });
      marker.addListener("click", (e: google.maps.MapMouseEvent) => {
        google.maps.event.addListenerOnce(
          this.$mapConfig.map,
          "click",
          (e: google.maps.MapMouseEvent) => {
            infowindow.close();
          }
        );
        if ("company_id" in this.$route.query) {
          infowindow.close();
          infowindow.open(this.$mapConfig.map, marker);
        } else {
          this.$router.push({
            name: "station-prefecture_id-name",
            params: { prefecture_id: station.prefecture_id,name: station.name },
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
  max-height: calc(var(--vh, 1vh) * 100 - 56px);
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
    max-height: 100vh;
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
  // @media screen and (max-width: 500px) {
  //   .map-container {
  //     max-height: calc(var(--vh, 1vh) * 100 - 120px);
  //   }
  // }
}
</style>
