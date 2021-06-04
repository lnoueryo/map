<template>
    <div>
        <right-drawer></right-drawer>
        <div id="container" :style="open?{paddingRight:256+'px'}:''">
            <main-view ref="view"></main-view>
        </div>
        <bottom-bar></bottom-bar>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import RightDrawer from '../components/RightDrawer.vue'
import MainView from '../components/MainView.vue'
import BottomBar from '../components/BottomBar.vue'
import practice from '~/assets/json/line/practice.json'
import Mixin from '~/utils/mixin.ts'
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, pref_name: string, station_name: string, station_lat: number, station_lon: number, line_name: string, order: number, company_name: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, line_name: string, polygon: LinePolyline[], color: string}
interface DataType {
    open: boolean,
    addMarker: LinePolyline[]
    // map: google.maps.Map | null,
    overview: google.maps.Map | null,
    index: number,
    polygon: google.maps.Polygon[] | null,
    polygons: google.maps.Polygon[][],
    stations: LinePolyline[],
    markers: google.maps.Marker[],
    // lines: Line[]
    polylines: google.maps.Polyline[],
}
export default Vue.extend({
    mixins: [Mixin],
    components: {
        MainView,
        RightDrawer,
        BottomBar
    },
    data(): DataType {
        return {
            open: false,
            addMarker: [],
            // map: null,
            overview: null,
            index: 0,
            polygon: null,
            polygons: [],
            stations: [],
            markers: [],
            polylines: [],
        }
    },
    computed:{
        lines(){
            return this.$store.getters['home/lines'];
        },
    },
    async created(){
        this.$store.dispatch('home/getLines')
    },
    mounted(){
        this.$on('open', (this as any).drawer);
    },
    methods:{
        drawer(){
            (this as any).open=!(this as any).open;
        },
        onClickResetPolyline(){
            this.$store.dispatch('resetPolyline', (this as any).polylines);
        },
        makeLineMarker(){
            practice.forEach((station: any,i: number)=>{
                let marker = (this as InstanceType<typeof Mixin>).makeMarker(station.lat, station.lng)
                marker.addListener("click", () => {
                    console.log(station.lat, station.lng, i)
                });
            })
        },
        makeLineArray(){
            let paths: {color: string, polygon: google.maps.LatLng[]}[] = [];
            (this as any).lines.forEach((line: Line)=>{
                let polygon: google.maps.LatLng[] = []
                line.polygon.forEach((coordinate: LinePolyline)=>{
                    polygon.push(new google.maps.LatLng(coordinate.lat, coordinate.lng))
                })
                paths.push({color: line.color, polygon: polygon})
            })
            paths.forEach((path)=>{
                (this as any).makePolyline(path)
            })
            const TOKYO_BOUNDS = {
                north: 35.760687,
                south: 35.530351,
                west: 139.2403931,
                east: 139.9368243,
            };
            (this as any).map.fitBounds( TOKYO_BOUNDS );
        },
        makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
            const polyline = new google.maps.Polyline( {
                map: (this as any).map,
                // path:practice,
                path:path.polygon,
                strokeColor: path.color,
                strokeOpacity: 0.9,
                strokeWeight: 3
            });
            const latLngBounds = new google.maps.LatLngBounds();
            polyline.getPath().forEach((latLng) => {
                latLngBounds.extend(latLng);
            });
            (this as any).polylines.push(polyline)
        },
    }
})
</script>

<style lang="scss">
    #container {
        height: 100%;
        width: 100%;
        position:relative;
        padding-right:100px;
        transition: all .3s;
    }
</style>