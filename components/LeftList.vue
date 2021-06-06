<template>
    <div>
        <div class="left-list" :style="{width: width+'px'}">
            <v-btn-toggle v-model="changeList" color="indigo" background-color="indigo">
                <v-btn>
                    <v-icon>mdi-train</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-information-outline</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-right</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-justify</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-justify</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-justify</v-icon>
                </v-btn>
            </v-btn-toggle>
            <div class="list-top">
                <div class="d-flex">
                    <search-bar ref="searchBar" placeholder="駅を検索" v-model="searchWord" @select="select(filteredSearchStations[0])">
                        <div class="menu" v-if="searchStations.length!==0" style="background-color:orange">
                            <div @mouseup.stop.prevent="select(searchStation)" v-for="(searchStation, i) in filteredSearchStations" :key="i" class="list">{{searchStation.station_name}}</div>
                        </div>
                    </search-bar>
                    <v-btn class="ml-1" icon color="indigo" @click="width=315"><v-icon>mdi-arrow-collapse-horizontal</v-icon></v-btn>
                </div>
                <div style="padding:10px">現在の表示件数<b>{{countMarkers}}</b>件</div>
            </div>
            <keep-alive>
                <div :is="component"></div>
            </keep-alive>
        <div style="position:absolute;top:0;bottom:0;right:-3px;width:6px;z-index:5;cursor:ew-resize;" @mousedown="dragStart"></div>
        </div>
    </div>
</template>

<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,station_lat:number,station_lon:number,station_name:string}
interface DataType {componentTypes:string[],countMarkers: number,searchWord:string|null,changeList:number,width:number};
interface DomEvent extends Event {clientX: number,clientY: number}
import Vue from 'vue';
import {mapGetters} from 'vuex'
import StationLines from '~/components/StationLines.vue';
import StationWiki from '~/components/StationWiki.vue';
import SearchBar from '~/components/SearchBar.vue';
export default Vue.extend({
    components:{
        StationLines,
        StationWiki,
        SearchBar
    },
    data(): DataType {
        return {
            componentTypes: ['station-lines', 'station-wiki', 'station-lines'],
            changeList: 0,
            countMarkers: 0,
            searchWord: null,
            width: 315,
        }
    },
    computed:{
        component(){
            return (this as any).componentTypes[(this as any).changeList];
        },
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
        hello(e: DomEvent){
            if (e.clientX<500&&e.clientX>100) {
                (this as any).width = e.clientX
            }
        },
        dragStart(){
            const that = this;
            const hello = (e: Event)=>{(that as any).hello(e)};
            this.$root.$el.addEventListener('mousemove',hello);
            this.$root.$el.addEventListener('mouseup',()=>{that.$root.$el.removeEventListener('mousemove',hello),{once:true}});
        },
        select(searchStation: Station){
            (this.$refs.searchBar as any).blur = false;
            (this.$refs.searchBar as any).$refs.input.blur();
            this.$store.dispatch('home/selectMarker',searchStation);
            this.$store.dispatch('home/getStationInfo', {name: searchStation.station_name})
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

<style lang="scss" scoped>
    .list{
        background-color:orange;
        text-align:left;
        padding: 8px 15px;
    }
    .left-list{
        height:100vh;
        width:100%;
        background-color: #363636;
        position:relative;
        max-height:calc(100vh - 114px);
        margin-bottom:100px
    }
    .list-top{
        padding:10px;
        padding-right:5px;
        text-align:center;
        border-radius:5px;
        color:#363636;
        background-color:white;
        position:relative;
        width:100%;
    }
</style>