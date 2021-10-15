<template>
    <div>
        <transition name="fade">
            <div class="middle-list" v-if="markerSwitch">
                <div v-if="markerSwitches.spots">
                    <div class="company-name">観光スポット</div>
                    <lists :list-title="cities" field="spots"></lists>
                </div>
                <div v-if="markerSwitches.stations">
                    <div class="company-name">駅</div>
                    <div v-for="(company, i) in companies" :key="i" style="position:relative">
                        <transition name="list">
                            <div v-if="isCheck(company.id, company.lines)"><label class="company-name" :for="company.name"><input :id="company.name" type="checkbox" :value="company" v-model="selectCompany" style="display:none;">{{company.name}}</label></div>
                        </transition>
                        <lists :firstInput="selectLine" @firstInput="selectLine = $event" @secondInput="selectStationMarker" :list-title="company.lines" field="stations"></lists>
                    </div>
                </div>
            </div>
        </transition>
    </div>
</template>


<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_id: number, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_id: number, id: number, line_id: number, order: number, pref_name: string, lat: number, lng: number, name: string}
interface Coordinate {lat: number, lng: number}
interface Spot {id: number, name: string, place_id: string, address: string, lat: number, lng: number, prefecture_id: string, city_code: string, geohash: string}
import Vue from 'vue';
const Lists = () => import('../../global/Lists.vue');
import { mapGetters } from 'vuex';
export default Vue.extend({
    components: {
        Lists,
    },
    computed: {
        ...mapGetters('old_city', [
            'lines',
            'filteredLines',
            'selectedMarker',
            'companies',
            'selectedCompanyItems',
            'selectedLineItems',
            'cities',
        ]),
        ...mapGetters('switch', [
            'markerSwitch',
            'markerSwitches'
        ]),
        selectCompany: {
            get() {
                return this.$store.getters['old_city/selectedCompanyItems']
            },
            set(value) {
                this.$store.dispatch('old_city/selectedCompanyItems', value)
            }
        },
        selectLine: {
            get() {
                return this.$store.getters['old_city/selectedLineItems']
            },
            set(value) {
                this.$store.dispatch('old_city/selectedLineItems', value)
            }
        }
    },
    methods:{
        selectStationMarker(obj: {name: string}) {
            this.$store.dispatch('info/getStationInfo', {name: obj.name});
            this.$store.dispatch('old_city/selectMarker', obj);
        },
        makeStationArray(lines: Line[]) {
            const stations: Coordinate[] = []
            lines.filter((line: {stations: Coordinate[]}) => {
                const filterStations = this.$mapConfig.boundsFilter(line.stations);
                filterStations.forEach((station: Coordinate) => {
                    stations.push(station)
                });
            })
            return stations
        },
        isCheck(id: number, lines: Line[]) {
            const filterLine: Line[] = this.filteredLines(lines);
            const stations = (this as any).makeStationArray(filterLine);
            return stations.some((station: Station) => {
                return station.company_id == id;
            })
        },
        select(searchStation: Station) {
            (this.$refs.searchBar as any).blur = false;
            (this.$refs.searchBar as any).$refs.input.blur();
            this.$store.dispatch('old_city/selectMarker',searchStation);
        },
        onClickList(station: Station) {
            this.$store.dispatch('info/getStationInfo',{name: station.name});
            this.$store.dispatch('old_city/selectMarker', station);
        },
        showInfoWindow(spot: Spot) {
            this.$mapConfig.createMapInfoWindow(spot.lat, spot.lng, spot.name)
        },
        hideInfoWindow() {
            this.$mapConfig.infoWindow.setMap(null)
        },
    }
})
</script>

<style lang="scss" scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }
    .middle-list {
        overflow-y: scroll;
        overflow-x: hidden;
        height: 100vh;
        max-height: calc(var(--vh, 1vh) * 100 - 250px);
        transition: all .5s;
        .company-name {
            text-align: center;
            border-radius: 5px;
            color: white;
            background-color: #363636;
            width: 100%;
            display: block;
            padding: 10px;
            transition: all .5s;
            cursor: pointer;
        }
        .company-name:hover {
            opacity: .7;
            transition: all .5s;
        }
        .company-name:active {
            opacity: .9;
            transition: all .5s;
        }
        .line-name {
            text-align: center;
            border-radius: 5px;
            color: white;
            width: 100%;
            display: block;
            padding: 10px;
            transition: all .5s;
            cursor: pointer;
        }
        .line-name:hover {
            opacity: .7;
            transition: all .5s
        }
        .line-name:active {
            opacity: .9;
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
        transition: all .5s;
        cursor: pointer;
    }
    .station-list:hover {
        opacity: 0.7;
        transition: all .5s;
    }
    .station-list:active {
        opacity: 0.9;
        transition: all .5s;
    }
</style>