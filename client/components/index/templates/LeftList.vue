<template>
    <div>
        <div class="left-list" :style="{width: width+'px'}">
            <v-btn-toggle mandatory v-model="changeList" color="indigo" background-color="#2f2f2f">
                <v-btn v-for="(button,i) in buttons" :key="i">
                    <v-icon>mdi-{{button}}</v-icon>
                </v-btn>
            </v-btn-toggle>
            <div class="list-top">
                <search-items ref="searchItem"></search-items>
            </div>
            <keep-alive>
                <transition name="fade">
                    <div :is="component"></div>
                </transition>
            </keep-alive>
        <div class="resize" @mousedown="dragStart"></div>
        </div>
    </div>
</template>

<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,lat:number,lng:number,name:string}
interface DataType {countMarkers: number,width:number,buttons: string[]};
interface DomEvent extends Event {clientX: number,clientY: number}
import Vue from 'vue';
import {mapGetters} from 'vuex';
const StationLines = () => import('../organisms/StationLines.vue');
const StationWiki = () => import('../organisms/StationWiki.vue');
const SearchItems = () => import('../organisms/SearchItems.vue');
const Event = () => import('../organisms/Event.vue');
const SearchBar = () => import('../../global/SearchBar.vue');
// import StationLines from '~/components/index/organisms/StationLines.vue';
// import StationWiki from '~/components/index/organisms/StationWiki.vue';
// import SearchItems from '~/components/index/organisms/SearchItems.vue';
// import Event from '~/components/index/organisms/Event.vue';
// import SearchBar from '~/components/global/SearchBar.vue';

export default Vue.extend({
    components:{
        StationLines,
        StationWiki,
        SearchBar,
        SearchItems,
        Event
    },
    data(): DataType {
        return {
            countMarkers: 0,
            width: 315,
            buttons: ['train', 'information-outline', 'format-align-right', 'format-align-justify']
        }
    },
    computed:{
        ...mapGetters('home', [
            'lines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
            'boundsFilter',
            'searchStations',
            'stationInfo',
            'showNumberOfMarkers'
        ]),
        component(){
            const componentTypes = ['station-lines', 'station-wiki', 'event'];
            return componentTypes[(this as any).changeList];
        },
        filteredSearchStations(){
            return this.searchStations.filter((_: any,index: number)=>{
                return index < 5;
            });
        },
        searchWord:{
            get(){
                return this.$store.getters['home/searchWord'];
            },
            set(newValue){
                this.$store.dispatch('home/searchWord',newValue);
            }
        },
        changeList:{
            get(){
                return this.$store.getters['home/changeList'];
            },
            set(newValue){
                this.$store.dispatch('home/changeList', newValue);
            }
        },
    },
    watch:{
        showNumberOfMarkers(newValue, OldValue){ //vuexの変化を検知
            (this as any).count(newValue, OldValue);
        },
    },
    methods:{
        limit(e: DomEvent){
            if (e.clientX<500&&e.clientX>100) {
                (this as any).width = e.clientX
            }
        },
        dragStart(){
            const that = this;
            const limit = (e: Event)=>{(that as any).limit(e)};
            this.$root.$el.addEventListener('mousemove',limit);
            this.$root.$el.addEventListener('mouseup',()=>{that.$root.$el.removeEventListener('mousemove',limit),{once:true}});
        },
        select(searchStation: Station){
            (this.$refs.searchBar as any).blur = false;
            (this.$refs.searchBar as any).$refs.input.blur();
            if(searchStation){
                this.$store.dispatch('home/selectMarker',searchStation);
                this.$store.dispatch('home/getStationInfo', {name: searchStation.name});
            } else {
                alert('見つかりませんでした')
            }
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
    }
})
</script>

<style lang="scss" scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
        transition: opacity .5s;
    }
    .resize{
        position:absolute;
        top:0;
        bottom:0;
        right:-3px;
        width:6px;
        z-index:5;
        cursor:ew-resize;
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