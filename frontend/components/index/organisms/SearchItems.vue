<template>
    <div>
        <div class="d-flex">
            <search-bar ref="searchBar" placeholder="駅を検索" v-model="searchWord" @select="select(filteredSearchStations[0])">
                <div class="menu" v-if="searchStations.length!==0" style="background-color:orange">
                    <div @mouseup.stop.prevent="select(searchStation)" v-for="(searchStation, i) in filteredSearchStations" :key="i" class="list">
                        <span>{{searchStation.name}}</span>
                    </div>
                </div>
            </search-bar>
            <div>
                <v-btn class="ml-1" icon color="indigo" @click="$parent.$data.width=315">
                    <v-icon>mdi-arrow-collapse-horizontal</v-icon>
                </v-btn>
            </div>
        </div>
        <div style="padding:10px">
            <span>現在の表示件数</span>
            <b v-if="markerSwitch">{{countMarkers}}</b>
            <b v-else>0</b>
            <span>件</span>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import {mapGetters} from 'vuex'
import SearchBar from '~/components/global/SearchBar.vue';
interface DataType {countMarkers: number};
interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,lat:number,lng:number,name:string};
export default Vue.extend({
    components:{
        SearchBar
    },
    data(): DataType {
        return {
            countMarkers: 0,
        }
    },
    computed:{
        ...mapGetters('home', [
            'searchStations',
            'stationInfo',
            'showNumberOfMarkers',
            'markerSwitch',
        ]),
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
    },
    watch:{
        showNumberOfMarkers(newValue, OldValue){ //vuexから表示されている数の変化を検知
            (this as any).count(newValue, OldValue);
        },
    },
    methods:{
        select(searchStation: Station){
            const searchBar = this.$refs.searchBar as InstanceType<typeof SearchBar>;
            searchBar.$data.blur = false;
            const input = searchBar.$refs.input as HTMLInputElement;
            input.blur();
            if(searchStation){
                this.$store.dispatch('home/selectMarker',searchStation);
                this.$store.dispatch('home/getStationInfo', {name: searchStation.name});
            } else {
                alert('見つかりませんでした')
            }
        },
        count(newValue: number, OldValue: number): void{
            const DURATION = 600
            const from = OldValue;
            const to = newValue;
            const startTime = Date.now()
            let timer = setInterval(() => {
                const elapsedTime = Date.now() - startTime
                const progress = elapsedTime / DURATION

                if (progress < 1) {
                    this.$data.countMarkers = Math.floor(from + progress * (to - from));
                } else {
                    clearInterval(timer);
                    this.$data.countMarkers = to;
                }
            }, 1)
        },
    }
})
</script>

<style lang="scss">
    .list{
        background-color:orange;
        text-align:left;
        padding: 8px 15px;
    }
</style>