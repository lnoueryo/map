<template>
    <div>
        <transition name="fade">
            <div class="middle-list" v-if="markerSwitch">
                <div v-if="markerSwitches.spots">
                    <div class="company-name">観光スポット</div>
                    <div v-for="(city, j) in cities" :key="j" style="position:relative;">
                        <transition name="list">
                            <div class="company-name" v-if="boundsFilter(city.spots).length !== 0">
                                {{city.name}}
                            </div>
                        </transition>
                        <transition-group name="list" tag="div">
                            <div class="station-list" style="width:100%;color:black" v-for="(spot, k) in boundsFilter(city.spots)" :key="k" @click="onClickList(spot)" @mouseover="showInfoWindow(spot)" @mouseout="hideInfoWindow">
                                <div>{{spot.name}}</div>
                            </div>
                        </transition-group>
                    </div>
                </div>
                <div v-if="markerSwitches.stations">
                    <div class="company-name">駅</div>
                    <div v-for="(company, i) in companies" :key="i" style="position:relative">
                        <transition name="list">
                            <div v-if="isCheck(company.id, company.lines)"><label class="company-name" :for="company.name"><input :id="company.name" type="checkbox" :value="company" v-model="selectCompany" style="display:none;">{{company.name}}</label></div>
                        </transition>
                        <div v-for="(line, j) in filteredLines(company.lines)" :key="j" style="color:black">
                            <transition name="list">
                                <div v-if="boundsFilter(line.stations).length!==0">
                                    <label class="line-name" :style="{backgroundColor: line.color}" :for="line.name"><input :id="line.name" type="checkbox" :value="line" v-model="selectLine" style="display:none;">{{line.name}}</label>
                                </div>
                            </transition>
                            <transition-group name="list" tag="div">
                                <div class="station-list" style="width:100%" v-for="(station, k) in boundsFilter(line.stations)" :key="k" @click="onClickList(station)">
                                <!-- <div style="width:100%" v-for="(station,k) in boundsFilter(line.stations)" :key="k" @click="onClickList(station)" :style="selectedMarker.name==station.name?{borderLeft: 'solid 5px orange',transition: 'all .5s'}:{transition: 'all .5s'}"> -->
                                    <div style="">{{station.name}}</div>
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
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_id: number, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_id: number, id: number, line_id: number, order: number, pref_name: string, lat: number, lng: number, name: string}

import Vue from 'vue';
const SearchBar = () => import('../../global/SearchBar.vue');
import { mapGetters } from 'vuex';
export default Vue.extend({
    components: {
        SearchBar
    },
    computed: {
        ...mapGetters('home', [
            'lines',
            'filteredLines',
            'selectedMarker',
            'boundsFilter',
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
                return this.$store.getters['home/selectedCompanyItems']
            },
            set(value) {
                this.$store.dispatch('home/selectedCompanyItems', value)
            }
        },
        selectLine: {
            get() {
                return this.$store.getters['home/selectedLineItems']
            },
            set(value) {
                this.$store.dispatch('home/selectedLineItems', value)
            }
        }
    },
    methods:{
        makeStationArray(lines: Line[]) {
            const stations: Station[] = []
            lines.filter((line) => {
                this.boundsFilter(line.stations).forEach((station: Station) => {
                    stations.push(station)
                });
            })
            return stations
        },
        isCheck(id: number, lines: Line[]) {
            const filterLine: Line[] = this.filteredLines(lines);
            const stations = this.makeStationArray(filterLine);
            return stations.some((station: Station) => {
                return station.company_id == id;
            })
        },
        select(searchStation: Station) {
            (this.$refs.searchBar as any).blur = false;
            (this.$refs.searchBar as any).$refs.input.blur();
            this.$store.dispatch('home/selectMarker',searchStation);
        },
        onClickList(station: Station) {
            this.$store.dispatch('info/getStationInfo',{name: station.name});
            this.$store.dispatch('home/selectMarker', station);
        },
        showInfoWindow(spot: any) {
            this.$mapConfig.createMapInfoWindow(spot.lat, spot.lng, spot.name)
        },
        hideInfoWindow(spot: any) {
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
        max-height: calc(100vh - 213px);
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