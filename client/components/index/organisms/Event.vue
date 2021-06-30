<template>
    <div>
        <transition name="fade">
            <div class="middle-list" v-if="markerSwitch">
                <transition-group name="list" tag="div">
                    <div class="my-1" style="width:100%" v-for="(event,k) in boundsFilter(events)" :key="k" @click="onClickList(event)">
                        <div style="padding:10px;background-color:white;width:100%;color:black;border-radius: 5px;">
                            <div>{{changeDate(event.started_at)}}</div>
                            <div><b>{{event.title}}</b></div>
                            <div>{{event.address}}</div>
                            <div>{{event.place}}</div>
                        </div>
                    </div>
                </transition-group>
            </div>
        </transition>
    </div>
</template>


<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_id: number, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_id: number,id:number,line_id:number,order:number,pref_name:string,lat:number,lng:number,name:string}

import Vue from 'vue';
import SearchBar from '../../global/SearchBar.vue';
import { mapGetters } from 'vuex';
export default Vue.extend({
    components:{
        SearchBar
    },
    computed:{
        ...mapGetters('home', [
            'lines',
            'events',
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
        },
    },
    async created(){
        this.$store.dispatch('home/getEvents');
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
        changeDate(date){
            const changeDateFormat = new Date(date);
            const month = changeDateFormat.getMonth() + 1;
            const day = changeDateFormat.getDate();
            const dayofweek = changeDateFormat.getDay();
            const dayname = ['日','月','火','水','木','金','土'];
            return month + '月' + day + '日' + '[' + dayname[dayofweek] + ']';
        }
        // onClickList(event: any){
        //     const latlng = new google.maps.LatLng(event.lat, event.lng);
        // }
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
    .middle-list{
        overflow-y:scroll;
        overflow-x:hidden;
        height:100vh;
        max-height:calc(100vh - 213px);
        transition: all .5s;
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