<template>
    <div style="display:flex;overflow:hidden;max-height:calc(100%-200px);">
        <left-list></left-list>
        <div style="position:relative;width:100%;">
            <map-view style="width:100%;height:100%;"></map-view>
            <!-- <line-chart style="position:absolute;top:0;bottom:0;right:0;left:0;"></line-chart> -->
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import LeftList from '../components/LeftList.vue'
import LineChart from '../components/LineChart.vue'
import MapView from '../components/Map.vue'
import polygonData from '~/assets/json/coordinates.json'
import Mixin from '~/utils/mixin.ts'
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, pref_name: string, station_name: string, station_lat: number, station_lon: number, line_name: string, order: number, company_name: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, line_name: string, polygon: LinePolyline[], color: string}
interface DataType {
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
    components:{
        LineChart,
        MapView,
        LeftList
    },
    data(): DataType {
        return {
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
    methods:{

        markerPosition(){
            // console.log(this.markers[0].setPosition(new google.maps.LatLng( 35.6666601740126, 139.35275529999995 )))
            // console.log(this.markers[0].position.lat.lat())
        },
        async check(){
            const bounds = (this as any).map.getBounds()
            const north = bounds.getNorthEast().lat();
            const south = bounds.getSouthWest().lat();
            const east = bounds.getNorthEast().lng();
            const west = bounds.getSouthWest().lng();
            const paramater = {params: {line_name: 'ＪＲ中央本線(東京－塩尻)',south: south, north: north,east: east, west: west}}
            const response = await this.$axios.$get('/api/map/station/line/', paramater);
            (this as any).makeStationsMarkers(response)
        },
        makeStationsMarkers(stations: Station[]){
            stations.forEach((station)=>{
                const marker = (this as InstanceType<typeof Mixin>).makeMarker(station.station_lat, station.station_lon);
                (this as any).markers.push(marker)
            })
        },
        async refresh(){
            const token = localStorage.getItem('token');
            const parsedToken = JSON.parse(token as string)
            const response = await this.$axios.$post('/api/token/refresh/', {refresh: parsedToken.refresh});
            this.$axios.setToken(response.access, 'Bearer')
        },
        setPolygons(){
            polygonData.forEach((city: Polygons,i: number)=>{
                let polygons: google.maps.Polygon[] = []
                city.polygons.forEach(coordinates => {
                    const polygon = new google.maps.Polygon({
                        paths: coordinates,
                        strokeColor: "#FF0000",
                        strokeOpacity: 0.5,
                        strokeWeight: 1.5,
                        fillColor: "#FF0000",
                        fillOpacity: 0.35,
                    });
                    const that = this;
                    google.maps.event.addListener(polygon, 'click', function() {
                        (that as InstanceType<typeof Mixin>).resetPoly(i)
                        // that.designatePolygon(i)
                    });
                    polygons.push(polygon);
                });
                (this as any).polygons.push(polygons as never)
            })
        },
        async clickMap(e: google.maps.MapMouseEvent){
            (this as InstanceType<typeof Mixin>).resetMapListeners('click')
            const latLng = {lat: e.latLng?.lat(), lng: e.latLng?.lng()};
            const response = await this.$axios.$post('/api/map/search-by-reverse-geocode', latLng as any);
            polygonData.forEach((city: Polygons, i: number) => {
                if (city.city == response.Property.AddressElement[1].Name) {
                    (this as InstanceType<typeof Mixin>).makePolygon(i)
                }
            });
            const that = this;
            setTimeout(()=>{
                (that as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
                    (that as any).clickMap(e)
                })
            },1500)
        },
        next(){
            (this as any).index +=1 as any
            (this as InstanceType<typeof Mixin>).resetPoly((this as any).index)
            (this as InstanceType<typeof Mixin>).makePolygon((this as any).index)
        },
        back(){
            (this as any).index -=1 as any
            (this as InstanceType<typeof Mixin>).resetPoly((this as any).index)
            (this as InstanceType<typeof Mixin>).makePolygon((this as any).index)
        },
    }
})
</script>
