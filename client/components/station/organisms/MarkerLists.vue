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
          :items="$store.getters['station/boundsFilter'](uniqueStations)"
          @item="selectStation($event)"
          v-if="'name' in $route.params === false"
        >
          <div>駅を選択</div>
        </simple-lists>
        <div v-else>
          <router-link :to="{name: 'station'}" class="company-name" >駅</router-link>
          <div
            v-for="(mainStation, i) in filteredCompanyLinesByparams"
            :key="i"
            style="position: relative"
          >
            <transition name="list">
              <div>
                <!-- <div v-if="isCheck(company.id, company.lines)"> -->
                <label class="company-name" :for="mainStation.company.name"
                  ><input
                    :id="mainStation.company.name"
                    type="checkbox"
                    :value="mainStation.company"
                    style="display: none"
                    @click="selectCompany(mainStation.company)"
                  />{{ mainStation.company.name }}</label
                >
              </div>
            </transition>
            <div
              v-for="(line, j) in mainStation.lines"
              :key="j"
              style="position: relative"
            >
              <transition name="list">
                <div
                  v-if="
                    $store.getters['station/boundsFilter'](line.stations)
                      .length !== 0
                  "
                >
                  <label
                    class="line-name"
                    :style="{ backgroundColor: line.color }"
                    :for="line.name"
                    @click="selectLine(company, line)"
                  >
                    {{ line.name }}
                  </label>
                </div>
              </transition>
              <transition-group name="list" tag="div">
                <div
                  class="station-list"
                  style="width: 100%; color: black"
                  v-for="(station, k) in $store.getters['station/boundsFilter'](
                    line.stations
                  )"
                  :key="k"
                >
                  <div>{{ station.name }}</div>
                </div>
              </transition-group>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>


<script lang="ts">
interface Polygon {
  lat: number;
  lng: number;
}
[];
interface Company {
  id: number;
  name: string;
  address: string;
  founded: string;
  lines: Line[];
}
interface Line {
  id: number;
  company_id: number;
  name: string;
  polygon: Polygon;
  color: string;
  stations: Station[];
}
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
interface Coordinate {
  lat: number;
  lng: number;
}

interface Prefecture {
  id: string;
  name: string;
  wiki: string;
  lat: number;
  lng: number;
  cities: City[];
}
interface City {
  name: string;
  wiki: string;
  city_code: string;
  province: string;
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
const Lists = () => import("../../global/Lists.vue");
const HalfModal = () => import("../../global/HalfModal.vue");
const WikiInfo = () => import("../../global/WikiInfo.vue");
import { mapGetters } from "vuex";
export default Vue.extend({
  components: {
    SimpleLists,
    Lists,
    HalfModal,
    WikiInfo,
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
    ...mapGetters("station", ["uniqueStations", "filteredCompanyLines", 'particularStations']),
    ...mapGetters("switch", ["leftListSwitch"]),
    filteredCompanyLinesByparams() {
      let filteredCompanyLines = JSON.parse(JSON.stringify(this.particularStations));
      if ("company_id" in this.$route.query) {
        filteredCompanyLines = filteredCompanyLines.filter(
          (station: Company) => {
            return String(station.company.id) == this.$route.query.company_id;
          }
        );
        if ("line_id" in this.$route.query) {
          const lineIds = (this.$route.query.line_id as string).split(",");
          filteredCompanyLines = filteredCompanyLines.map(
            (station: Company) => {
              station.lines = station.lines.filter((line) => {
                return lineIds.includes(String(line.id));
              });
              return station;
            }
          );
        }
      }
      return filteredCompanyLines;
    },
  },
  methods: {
    back() {
      const query = { ...{}, ...this.$route.query } as any;
      const queryArray = Object.keys(this.$route.query);
      if (queryArray.length !== 0) delete query[queryArray.slice(-1)[0]];
      delete query[queryArray.slice(-1)[0]];
      this.$router.push({ query: query });
    },
    makeStationArray(lines: Line[]) {
      const stations: Coordinate[] = [];
      lines.filter((line: { stations: Coordinate[] }) => {
        const filterStations = this.$mapConfig.boundsFilter(line.stations);
        filterStations.forEach((station: Coordinate) => {
          stations.push(station);
        });
      });
      return stations;
    },
    selectCompany(company: Company) {
      if('company_id' in this.$route.query) {
        this.$router.push({
          name: "station-prefecture_id-name",
          params: { name: this.$route.params.name },
        });
      } else {
        this.$router.push({
          name: "station-prefecture_id-name",
          params: { name: this.$route.params.name },
          query: { company_id: String(company.id) },
        });
      }
    },
    selectLine(company: Company, line: Line) {
      if('line_id' in this.$route.query) {
        this.$router.push({
          name: "station-prefecture_id-name",
          params: { name: this.$route.params.name },
          query: { company_id: String(company.id) },
        });
      } else {
        this.$router.push({
          name: "station-prefecture_id-name",
          params: { name: this.$route.params.name },
          query: { company_id: String(company.id), line_id: String(line.id) },
        });
      }
    },
    selectStation(station: Station) {
      this.$router.push({
        name: "station-prefecture_id-name",
        params: { name: station.name },
      });
    },
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
.middle-list {
  overflow-y: scroll;
  overflow-x: hidden;
  height: 100vh;
  max-height: calc(var(--vh, 1vh) * 100 - 213px);
  transition: all 0.5s;
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
    text-decoration: none;
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
.station-list {
  padding: 10px;
  background-color: white;
  width: 100%;
  transition: all 0.5s;
  cursor: pointer;
}
.station-list:hover {
  opacity: 0.7;
  transition: all 0.5s;
}
.station-list:active {
  opacity: 0.9;
  transition: all 0.5s;
}
</style>