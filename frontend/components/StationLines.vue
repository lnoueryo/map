<template>
    <div>
        <div class="middle-list">
            <div v-for="(company, i) in companies" :key="i" style="position:relative">
                <transition name="list">
                    <div :style="selectCompany.length!==0?{borderLeft: 'solid 5px orange',transition: 'all .5s'}:{transition: 'all .5s'}" v-if="isCheck(company.id, company.lines)"><label class="company-name" :for="company.name"><input :id="company.name" type="checkbox" :value="company" v-model="selectCompany" style="display:none;">{{company.name}}</label></div>
                </transition>
                <div v-for="(line, j) in filteredLines(company.lines)" :key="j" style="color:black">
                    <transition name="list">
                        <div v-if="boundsFilter(line.stations).length!==0">
                            <label class="line-name" :style="{backgroundColor: line.color}" :for="line.name"><input :id="line.name" type="checkbox" :value="line" v-model="selectLine" style="display:none;">{{line.name}}</label>
                        </div>
                    </transition>
                    <transition-group name="list" tag="div">
                        <div style="width:100%" v-for="(station,k) in boundsFilter(line.stations)" :key="k" @click="onClickList(station)" :style="selectedMarker.name==station.name?{borderLeft: 'solid 5px orange',transition: 'all .5s'}:{transition: 'all .5s'}">
                            <div style="padding:10px;background-color:white;width:100%">{{station.name}}</div>
                        </div>
                    </transition-group>
                </div>
            </div>
        </div>
    </div>
</template>


<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_id: number, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_id: number,id:number,line_id:number,order:number,pref_name:string,lat:number,lng:number,name:string}
interface DataType {countMarkers: number,searchWord:string|null};
interface Company {id: number, name: string, address: string, founded: string, lines: Line[]};

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
    //  @click="selectedItems(company)"
    computed:{
        ...mapGetters('home', [
            'lines',
            'filteredLines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
            'boundsFilter',
            'stationInfo',
            'companies',
            'selectedCompanyItems',
            'selectedLineItems',
        ]),
        selectCompany:{
            get(){
                return this.$store.getters['home/selectedCompanyItems']
            },
            set(value){
                this.$store.dispatch('home/selectedCompanyItems', value)
            }
        },
        selectLine:{
            get(){
                return this.$store.getters['home/selectedLineItems']
            },
            set(value){
                this.$store.dispatch('home/selectedLineItems', value)
            }
        }
    },
    watch:{
        searchWord(newValue){
            this.$store.dispatch('home/searchWord',newValue)
        }
    },
    methods:{
        makeStationArray(lines: Line[]){
            const stations: Station[] = []
            lines.filter((line)=>{
                this.boundsFilter(line.stations).forEach((station: Station) => {
                    stations.push(station)
                });
            })
            return stations
        },
        isCheck(id: number,lines: Line[]){
            const filterLine: Line[] = this.filteredLines(lines);
            const stations = (this as any).makeStationArray(filterLine);
            return stations.some((station: Station)=>{
                return station.company_id==id;
            })
        },
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
            this.$store.dispatch('home/getStationInfo',{name: station.name})
            this.$store.dispatch('home/selectMarker', station);
        }
    }
})
</script>

<style lang="scss" scoped>
    .middle-list{
        overflow-y:scroll;
        overflow-x:hidden;
        height:100vh;
        max-height:calc(100vh - 213px);
        .company-name{
            text-align:center;
            border-radius:5px;
            color:white;
            background-color:#363636;
            width:100%;
            display: block;
            padding:10px;
        }
        .line-name{
            text-align:center;
            border-radius:5px;
            color:white;
            width:100%;
            display: block;
            padding:10px;
        }
        .list-move{
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
            position:absolute;
        }
        .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
            opacity: 0;
            transform: translateX(256px);
        }
    }
</style>