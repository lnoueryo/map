<template>
    <div>
        <div class="d-flex">
            <search-bar ref="searchBar" placeholder="駅を検索" v-model="searchWord">
                <!-- <div class="menu" v-if="searchStations.length !== 0" style="background-color: white">
                    <div @mouseup.stop.prevent="select(searchStation)" v-for="(searchStation, i) in filteredSearchStations" :key="i" class="list">
                        <span>{{searchStation.name}}</span>
                    </div>
                </div> -->
            </search-bar>
            <div>
                <v-btn class="ml-1" icon color="indigo" @click="$parent.$data.width=345">
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
import {mapGetters} from 'vuex';
const SearchBar = () => import('../../global/SearchBar.vue');
const ToggleSwitch = () => import('../../global/ToggleSwitch.vue');

interface DataType {countMarkers: number};
interface Station {company_name: string, id: number, line_name: string, order: number, pref_name: string, lat: number, lng: number, name: string};
export default Vue.extend({
    components:{
        SearchBar,
        ToggleSwitch
    },
    data(): DataType {
        return {
            countMarkers: 0,
        }
    },
    computed: {
        ...mapGetters('home', [
            // 'showNumberOfMarkers',
        ]),
        ...mapGetters('switch', [
            'markerSwitch',
        ]),
        searchWord: {
            get() {
                return this.$store.getters['home/searchWord'];
            },
            set(newValue) {
                this.$store.dispatch('home/searchWord', newValue);
            }
        },
    },
    // watch: {
    //     showNumberOfMarkers(newValue, OldValue) { //vuexから表示されている数の変化を検知
    //         (this as any).count(newValue, OldValue);
    //     },
    // },
    methods: {
        select(searchStation: Station) {
            const searchBar = this.$refs.searchBar as any;
            // const searchBar = this.$refs.searchBar as InstanceType<typeof SearchBar>;
            searchBar.$data.blur = false;
            const input = searchBar.$refs.input as HTMLInputElement;
            input.blur();
            if(searchStation){
                this.$store.dispatch('home/selectMarker', searchStation);
                this.$store.dispatch('info/getStationInfo', {name: searchStation.name});
                this.$store.dispatch('info/getTwitterInfo', {name: searchStation.name});
            } else {
                alert('見つかりませんでした')
            }
        },
        count(newValue: number, OldValue: number): void {
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

<style lang="scss" scoped>
    .list {
        background-color: orange;
        text-align: left;
        padding: 8px 15px;
        cursor: pointer;
        color: rgb(99, 61, 61);
        transition: all .5s;
        // border-color: black;
        // outline: 0;
        // box-shadow: inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(102, 175, 233, .6);
    }
    .list:hover {
        opacity: 0.7;
        text-align: left;
        padding: 8px 15px;
        transition: all .5s;
    }
    .list:active {
        color: rgb(0, 0, 0);
        opacity: 0.8;
        transition: all .5s;
    }
    .w50 {
        width: 50%;
    }
</style>