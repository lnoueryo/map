<template>
    <div>
        <div class="list-top">
            <div>
                <search-bar ref="searchBar" placeholder="駅を検索" v-model="searchWord" @select="select(filteredSearchStations[0])">
                    <div class="menu" v-if="searchStations.length!==0" style="background-color:orange">
                        <div @mouseup.stop.prevent="select(searchStation)" v-for="(searchStation, i) in filteredSearchStations" :key="i" class="list">{{searchStation.station_name}}</div>
                    </div>
                </search-bar>
            </div>
            <div style="padding:10px" v-if="showNumberOfMarkers!==0">現在の表示件数<b>{{countMarkers}}</b>件</div>
        </div>
        <div class="middle-list">
            <div v-for="(line, i) in lines" :key="i" style="color:black">
                <transition name="list">
                    <div v-if="boundsFilter(line.stations).length!==0" style="padding:10px;text-align:center;border-radius:5px;color:white;" :style="{backgroundColor: line.color}">{{line.line_name}}</div>
                </transition>
                <transition-group name="list" tag="div">
                    <div v-for="(station,j) in boundsFilter(line.stations)" :key="j" @click="onClickList(station)" :style="selectedMarker.station_name==station.station_name?{borderLeft: 'solid 5px orange',transition: 'all .5s'}:{transition: 'all .5s'}">
                        <div style="padding:10px;background-color:white;">{{station.station_name}}</div>
                    </div>
                </transition-group>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, line_name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,station_lat:number,station_lon:number,station_name:string}
interface DataType {countMarkers: number,searchWord:string|null};
import Vue from 'vue';
import SearchBar from '~/components/SearchBar.vue';
import { mapGetters } from 'vuex';
export default Vue.extend({
    components:{
        SearchBar
    },
    data(): DataType {
        return {
            countMarkers: 0,
            searchWord: null,
        }
    },
    computed:{
        filteredSearchStations(){
            return this.searchStations.filter((_: any,index: number)=>{
                return index < 5;
            });
        },
        ...mapGetters('home', [
            'lines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
            'showNumberOfMarkers',
            'boundsFilter',
            'searchStations',
            'stationInfo',
        ]),
    },
    watch:{
        showNumberOfMarkers(newValue, OldValue){
            (this as any).count(newValue, OldValue);
        },
        searchWord(newValue){
            this.$store.dispatch('home/searchWord',newValue)
        }
    },
    methods:{
        select(searchStation: Station){
            (this.$refs.searchBar as any).blur = false;
            (this.$refs.searchBar as any).$refs.input.blur();
            this.$store.dispatch('home/selectMarker',searchStation)
        },
        count(newValue: number, OldValue: number){
            const DURATION = 600

            const from = OldValue;
            const to = newValue;
            const startTime = Date.now()
            const that = this;
            let timer = setInterval(() => {
                const elapsedTime = Date.now() - startTime
                const progress = elapsedTime / DURATION

                if (progress < 1) {
                    (this as any).countMarkers = Math.floor(from + progress * (to - from));
                } else {
                    clearInterval(timer);
                    (this as any).countMarkers = to;
                }
            }, 1)
        },
        onClickList(station: Station){
            this.$store.dispatch('home/getStationInfo',{name: station.station_name})
            this.$store.dispatch('home/selectMarker', station);
        }
    }
})
</script>

<style lang="scss">
    .list-top{
        padding:10px;
        padding-right:25px;
        text-align:center;
        border-radius:5px;
        color:#363636;
        background-color:white;
        position:relative;
        width:100%;
    }
    .middle-list{
        overflow-y:scroll;
        overflow-x:hidden;
        height:100vh;
        max-height:calc(100vh - 213px);
    }
</style>