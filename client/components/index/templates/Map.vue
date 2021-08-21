<template>
    <div class="map-container">
        <map-top class="map-top"></map-top>
        <line-chart class="line-chart" v-if="chartSwitch"></line-chart>
        <div id="map" ref="map" :class="{'show-line' : chartSwitch}"></div>
        <div class="dot" v-if="dotSwitch"></div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';
const LineChart = () => import('../organisms/LineChart.vue');
const MapTop = () => import('../organisms/MapTop.vue');

interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number,city_code: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string,stations: Station[]}
interface DataType {addMarker: { lat: number; lng: number; }[],map: google.maps.Map|null, overview: google.maps.Map|null, overviewConfig: {difference: number,maxZoom: number, minZoom: number},markers: google.maps.Marker[][],polylines: google.maps.Polyline[],polygons: google.maps.Polygon[][],exponentialBackoff:number,timer: null|NodeJS.Timer}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
export default Vue.extend({
    components: {
        LineChart,
        MapTop
    },
    data(): DataType {
        return {
            map: null,
            overview: null,
            overviewConfig: {difference: 5,maxZoom: 13, minZoom: 3},
            markers: [],
            polylines: [],
            addMarker: [],
            polygons: [],
            exponentialBackoff: 1000,
            timer: null
        }
    },
    computed:{
        ...mapGetters('home', [
            'companies',
            'lines',
            'events',
            'changeList',
            'filteredLines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'chartSwitch',
            'dotSwitch',
            'selectedMarker',
            'stationInfo',
            'removeOverlap',
            'cities',
            'selectedCityItems',
        ])
    },
    watch:{
        lines:{
            handler(v){
                if (this.markerSwitch) {
                    this.makeLineMarker(v);
                }
                if (this.lineSwitch) {
                    this.makeLineArray(v);
                }
            },
        },
        selectedCityItems:{
            handler(v){
                this.makeCityPolygon(v)
            },
        },
        markerSwitch:{
            handler(value){
                if (value) {
                    const that = this;
                    let timer = setInterval(function(){
                        if (google) {
                            clearInterval(timer);
                            that.makeLineMarker(that.lines);
                        }
                    }, 100);
                } else {
                    this.$mapConfig.resetMarkers(this.markers)
                }
            },
            immediate: true,
        },
        lineSwitch:{
            handler(value){
                if (value) {
                    const that = this;
                    let timer = setInterval(function(){
                        if (google) {
                            clearInterval(timer);
                            that.makeLineArray(that.lines);
                        }
                    }, 100);
                } else {
                    this.$mapConfig.resetPolyline(this.polylines)
                }
            },
            immediate: true
        },
        // changeList:{
        //     handler(value){
        //         if (this.markerSwitch) {
        //             if (value == 2) {
        //                 const that = this;
        //                 let timer = setInterval(function(){
        //                     if (that.events.length !== 0) {
        //                         clearInterval(timer)
        //                         that.makeEventMarker(that.events);
        //                     }
        //                 }, 100)
        //             } else {
        //                 this.makeLineMarker(this.lines);
        //             }
        //         }
        //     },
        //     immediate: true,
        // },
        selectedMarker(v){
            this.focusMarker(v);
        },
    },
    mounted(){
        console.log(this.$mapConfig.mapOptions())
        this.setMap().then(()=>{
            let timer: NodeJS.Timer|null;
            this.$mapConfig.map.addListener("bounds_changed", () => {
                const bounds = this.$mapConfig.currentBounds(this.$mapConfig.map)
                const that = this;
                if(timer!==null){
                    clearTimeout(timer)
                }
                timer = setTimeout(function(){
                    const getMapCenter = that.$mapConfig.map.getCenter();
                    const mapCenter = {lat: getMapCenter.lat(), lng: getMapCenter.lng()};
                    const zoom = that.$mapConfig.map.getZoom();
                    that.$store.dispatch('home/getCity', {mapCenter:mapCenter, zoom:zoom});
                    that.$store.dispatch('home/getCurrentBounds', bounds);
                },750);
            });
            this.addClickMapListeners()
        })
    },
    methods:{
        async setMap(){
            try {
                const mapEl = this.$refs.map;
                this.$mapConfig.makeMap(mapEl as HTMLElement)
                this.exponentialBackoff = 1000;
            } catch (error) {
                const that = this;
                this.exponentialBackoff*2
                let timer = setTimeout(function(){that.setMap()},that.exponentialBackoff)
                if(this.exponentialBackoff>=8000){
                    clearInterval(timer);
                    this.exponentialBackoff = 1000;
                    alert('some kind of error happened');
                }
            }
        },
        makeCityPolygon(v: City[]){
            const polygons = v.map((selectedCityItem: City, index: number)=>{
                return selectedCityItem.polygons.map((polygon)=>{
                    return this.makePolygon(polygon, index);
                })
            })
            if (this.polygons.length !== 0) {
                this.resetPoly(this.polygons);
            }
            const that = this;
            setTimeout(function(){
                that.polygons = polygons;
            },100)
        },
        onClickMap(e: google.maps.MapMouseEvent){
            google.maps.event.clearListeners(this.$mapConfig.map, 'click');
            this.$store.dispatch('home/searchCityCode',e).then(()=>{this.addClickMapListeners()});
        },
        makePolygon(coordinates: {lat: number,lng: number}[], i: number){
            const polygon = new google.maps.Polygon({
                paths: coordinates,
                strokeColor: "red",
                strokeOpacity: 0.5,
                strokeWeight: 2,
                fillColor: "#00bb93",
                fillOpacity: 0.3,
            });
            const that = this;
            google.maps.event.addListener(polygon, 'click', function(e: google.maps.MapMouseEvent) {
                that.onClickMap(e);
            });
            polygon.setMap(this.$mapConfig.map);
            return polygon
        },
        resetPoly(polygons: google.maps.Polygon[][]){
            polygons.forEach(cityPolygon => {
                cityPolygon.forEach(polygon => {
                    polygon.setMap(null)
                });
            });
        },
        resetMapListeners(...arg: string[]){
            arg.forEach(event => {
                google.maps.event.clearListeners(this.$mapConfig.map, event);
            });
        },
        addClickMapListeners(){
            this.$mapConfig.map.addListener('click', (e: google.maps.MapMouseEvent)=>{
                this.clearTime()
                const that = this;
                this.timer = setTimeout(function(){
                    that.onClickMap(e);
                },360)
            })
        },
        focusMarker(station: Station){
            this.$mapConfig.map.setZoom(16);
            const latLng = new google.maps.LatLng(station.lat, station.lng);
            this.$mapConfig.map.panTo(latLng);
        },
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
        onClickResetPolyline(){
            this.$mapConfig.resetPolyline(this.polylines);
        },
        async makeLineMarker(lines: Line[]){
            const markers: google.maps.Marker[][] = [];
            await lines.forEach((line: any,i: number)=>{
                const lineMarkerArray: google.maps.Marker[] = [];
                line.stations.forEach((station: Station)=>{
                    let marker = this.makeMarker(station);
                    marker.addListener("click", () => {
                        this.$store.dispatch('home/selectMarker',station);
                        this.$store.dispatch('home/getTwitterInfo', {name: station.name + '駅'});
                        this.$store.dispatch('home/getStationInfo', {name: station.name + '駅'})
                        .then(() => {
                            this.$store.commit('home/searching', false)
                        });
                    });
                    lineMarkerArray.push(marker);
                });
                markers.push(lineMarkerArray)
            });
            const that = this;
            setTimeout(function(){
                that.$mapConfig.resetMarkers(that.markers)
                .then(()=>{that.markers = markers;})
            },1000)
        },
        async makeEventMarker(events: any){
            const eventMarkerArray: google.maps.Marker[] = [];
            await events.forEach((event: Station)=>{
                let marker = this.makeMarker(event);
                marker.addListener("click", () => {
                    this.$store.dispatch('home/selectMarker',event);
                });
                eventMarkerArray.push(marker);
            });
            const that = this;
            setTimeout(async () => {
                await that.$mapConfig.resetMarkers(that.markers)
                that.markers = [eventMarkerArray];
            },2000)
        },
        makeMarker(station: Station){
            let img = '';
            const marker = new google.maps.Marker({
                map: this.$mapConfig.map,
                position: new google.maps.LatLng(station.lat, station.lng),
                icon: img,
                // optimized: true,
            });
            return marker
        },
        makeLineArray(lines: Line[]){
            this.$mapConfig.resetPolyline(this.polylines)
            let paths: {name: string, color: string, polygon: google.maps.LatLng[]}[] = [];
            lines.forEach((line: Line)=>{
                let polygon: google.maps.LatLng[] = [];
                line.polygon.forEach((coordinate: LinePolyline)=>{
                    polygon.push(new google.maps.LatLng(coordinate.lat, coordinate.lng));
                });
                paths.push({name: line.name, color: line.color, polygon: polygon});
            });
            const that = this;
            paths.forEach((path)=>{
                const polyline = (this as any).makePolyline(path);
                polyline.addListener("click", () => {
                    const latLngBounds = new google.maps.LatLngBounds();
                    polyline.getPath().forEach((latLng: google.maps.LatLng) => {
                        latLngBounds.extend(latLng);
                    });
                    that.$mapConfig.map.fitBounds( latLngBounds ) ;
                });
            });
        },
        makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
            const polyline = new google.maps.Polyline({
                map: this.$mapConfig.map,
                path:path.polygon,
                strokeColor: path.color,
                strokeOpacity: 0.9,
                strokeWeight: 3
            });
            // const latLngBounds = new google.maps.LatLngBounds();
            // polyline.getPath().forEach((latLng) => {
            //     latLngBounds.extend(latLng);
            // });
            (this as any).polylines.push(polyline);
            return polyline;
        },
        clearTime(){
            if (this.timer) {
                clearTimeout(this.timer)
            }
        }
    }
})
</script>

<style lang="scss" scoped>
.map-container{
    position:relative;
    width:100%;
    height:100vh;
    max-height:calc(100vh - 64px);
    .line-chart{
        position: absolute;
        top:40px;
        bottom: 0;
        right: 0;
        left: 0;
        margin: auto;
    }
    .map-top{
        position:absolute;
        z-index: 1;
    }
    .dot {
        position:absolute;
        top:0;
        bottom:0;
        left:0;
        right:0;
        margin:auto;
        width:9px;
        height:9px;
        border-radius:50%;
        background-color:red;
        opacity:0.4;
        transition: all 2s;
    }
    #map {
        width: 100%;
        height: 100%;
        position: relative;
        // padding-top: 56.25%;
        transition: all .5s
    }
    .show-line{
        opacity: 0.4;
    }
    #overview-wrapper{
        position:absolute;
        width: 30%;
        bottom: 50px;
        left: 15px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
        #overview-container {
            position: relative;
            width: 100%;
            #overview {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }
        }
        #overview-container:before {
            content:"";
            display: block;
            padding-top: 56.25%;
        }
    }
    @media screen and (max-width: 500px) {
        .map-top {
            top: 50px;
        }
        .line-chart{
            top:100px;
        }
    }
}
</style>