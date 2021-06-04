<template>
    <div>
        <div class="left-list">
            <div>
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
    </div>
</template>

<script lang="ts">

interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,station_lat:number,station_lon:number,station_name:string}
import Vue from 'vue';
import { mapGetters } from 'vuex';
export default Vue.extend({
    computed:{
        ...mapGetters('home', [
            'lines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
        ])
    },
    methods:{
        boundsFilter(stations: Station[]){
            const filteredStations = stations.filter((station)=>{
                const verticalCondition = this.bounds.west < station.station_lon && this.bounds.east > station.station_lon;
                const horizonalCondition = this.bounds.south < station.station_lat && this.bounds.north > station.station_lat;
                return verticalCondition && horizonalCondition;
            });
            return filteredStations;
        },
        onClickList(station: Station){
            console.log(station)
            this.$store.dispatch('home/selectMarker', station)
        }
    }
})
</script>

<style lang="scss">
    .left-list{
        height:100vh;
        min-width:256px;
            background-color: #363636;
        position:relative;
        max-height:calc(100vh - 114px);
        overflow-y: scroll;
        overflow-x: hidden;
        max-width: 256px;
    }
    .list-enter-active, .list-leave-active {
        transition: all 1s;
    }
    .list-enter, .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
        opacity: 0;
        transform: translateX(256px);
    }
</style>