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
 interface GMapWindow extends Window {
   google: any;
}
declare const window: GMapWindow;
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number,city_code: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string,stations: Station[]}
interface DataType {addMarker: { lat: number; lng: number; }[], trainIcon: {small: string, big: string}, spotIcon: {small: string, big: string}, overview: google.maps.Map|null, overviewConfig: {difference: number,maxZoom: number, minZoom: number},stationsMarkers: google.maps.Marker[][],spotsMarkers: google.maps.Marker[][],polylines: google.maps.Polyline[],polygons: google.maps.Polygon[][],timer: null|NodeJS.Timer}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Words   {code: string, province: string, lat: string, lng: string, city: string, spots: {name: string, place_id: string, address: string, lat: string, lng: string}}

export default Vue.extend({
    components: {
        LineChart,
        MapTop
    },
    data(): DataType {
        return {
            overview: null,
            trainIcon: {small: require('~/assets/img/train.png'), big: require('~/assets/img/station.png')},
            spotIcon: {small: require('~/assets/img/spot_small.png'), big: require('~/assets/img/spot.png')},
            overviewConfig: {difference: 5,maxZoom: 13, minZoom: 3},
            stationsMarkers: [],
            spotsMarkers: [],
            polylines: [],
            addMarker: [],
            polygons: [],
            timer: null
        }
    },
    computed:{
        ...mapGetters('home', [
            'lines',
            'words',
            'events',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'chartSwitch',
            'dotSwitch',
            'selectedMarker',
            'selectedCityItems',
            'stationSwitch',
            'spotSwitch',
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
                    let timer = setInterval(() => {
                        if (window.google) {
                            clearInterval(timer);
                            that.makeLineMarker(that.lines);
                            that.makeSpots(that.words)
                        }
                    }, 100);
                } else {
                    this.$mapConfig.resetMarkers(this.stationsMarkers)
                    this.$mapConfig.resetMarkers(this.spotsMarkers)
                }
            },
            immediate: true,
        },
        lineSwitch:{
            handler(value){
                if (value) {
                    const that = this;
                    let timer = setInterval(function(){
                        if (window.google) {
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
        selectedMarker(v){
            const zoom = 16
            this.$mapConfig.focusMarker(v, zoom);
        },
    },
    async mounted(){
        await this.setMap()
        let timer: NodeJS.Timer|null;
        this.$mapConfig.map.addListener("bounds_changed", () => {
            const bounds = this.$mapConfig.currentBounds(this.$mapConfig.map)
            const getMapCenter = this.$mapConfig.map.getCenter();
            const mapCenter = {lat: getMapCenter.lat(), lng: getMapCenter.lng()};
            const zoom = this.$mapConfig.map.getZoom();
            const that = this;
            if(timer!==null){
                clearTimeout(timer)
            }
            timer = setTimeout(function(){
                that.$store.dispatch('home/getCity', {mapCenter: mapCenter, zoom: zoom});
                that.$store.dispatch('home/getCurrentBounds', bounds);
            },750);
            (zoom > 13) ? this.$mapConfig.changeIcon(this.stationsMarkers, this.trainIcon.big) : this.$mapConfig.changeIcon(this.stationsMarkers, this.trainIcon.small);
            (zoom > 13) ? this.$mapConfig.changeIcon(this.spotsMarkers, this.spotIcon.big) : this.$mapConfig.changeIcon(this.spotsMarkers, this.spotIcon.small);
        });
        this.addClickMapListeners()
        this.makeSpots(this.words)
    },
    methods:{
        async setMap() {
            const mapEl = this.$refs.map;
            this.$mapConfig.makeMap(mapEl as HTMLElement)
        },
        async makeSpots(words: Words[]) {
            if(this.spotSwitch) {
                const markers: google.maps.Marker[][] = [];
                await words.forEach((word: any, i: number) => {
                    const spotMarkerArray: google.maps.Marker[] = [];
                    word.spots.forEach((spot: Station) => {
                        let marker = this.$mapConfig.makeMarker(spot, this.spotIcon.big);
                        marker.addListener("click", async () => {
                            this.$store.dispatch('home/selectMarker', spot);
                            this.$store.dispatch('home/getTwitterInfo', {name: spot.name});
                            // await this.$store.dispatch('home/getStationInfo', {name: spot.name})
                            this.$store.commit('home/searching', false)
                        });
                        spotMarkerArray.push(marker);
                    });
                    markers.push(spotMarkerArray)
                });
                const that = this;
                setTimeout(async () => {
                    await that.$mapConfig.resetMarkers(that.spotsMarkers)
                    that.spotsMarkers = markers;
                },1000)
            }
        },
        makeCityPolygon(v: City[]) {
            const polygons = v.map((selectedCityItem: City, index: number) => {
                return selectedCityItem.polygons.map((polygon_obj) => {
                    const polygon = this.$mapConfig.makePolygon(polygon_obj, index);
                    window.google.maps.event.addListener(polygon, 'click', function(e: google.maps.MapMouseEvent) {
                        that.onClickMap(e);
                    });
                    return polygon
                })
            })
            if (this.polygons.length !== 0) {
                this.$mapConfig.resetPolygon(this.polygons);
            }
            const that = this;
            setTimeout(() => {
                that.polygons = polygons;
            },100)
        },
        async onClickMap(e: google.maps.MapMouseEvent) {
            window.google.maps.event.clearListeners(this.$mapConfig.map, 'click');
            await this.$store.dispatch('home/searchCityCode', e);
            this.addClickMapListeners();
        },
        resetMapListeners(...arg: string[]) {
            arg.forEach(event => {
                window.google.maps.event.clearListeners(this.$mapConfig.map, event);
            });
        },
        addClickMapListeners() {
            this.$mapConfig.map.addListener('click', (e: google.maps.MapMouseEvent) => {
                this.clearTime()
                const that = this;
                this.timer = setTimeout(() => {
                    that.onClickMap(e);
                },360)
            })
        },
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
        onClickResetPolyline() {
            this.$mapConfig.resetPolyline(this.polylines);
        },
        async makeLineMarker(lines: Line[]) {
            if(this.stationSwitch) {
                const markers: google.maps.Marker[][] = [];
                await lines.forEach((line: any,i: number) => {
                    const lineMarkerArray: google.maps.Marker[] = [];
                    line.stations.forEach((station: Station) => {
                        let marker = this.$mapConfig.makeMarker(station, this.trainIcon.big);
                        marker.addListener("click", async () => {
                            this.$store.dispatch('home/selectMarker',station);
                            this.$store.commit('home/twitterInfo', []);
                            this.$store.dispatch('home/getTwitterInfo', {name: station.name + '駅'});
                            await this.$store.dispatch('home/getStationInfo', {name: station.name + '駅'})
                            this.$store.commit('home/searching', false)
                        });
                        lineMarkerArray.push(marker);
                    });
                    markers.push(lineMarkerArray)
                });
                const that = this;
                setTimeout(async () => {
                    await that.$mapConfig.resetMarkers(that.stationsMarkers)
                    that.stationsMarkers = markers;
                },1000)
            }
        },
        makeLineArray(lines: Line[]) {
            this.$mapConfig.resetPolyline(this.polylines)
            let paths: {name: string, color: string, polygon: google.maps.LatLng[]}[] = [];
            lines.forEach((line: Line) => {
                let polygon: google.maps.LatLng[] = [];
                line.polygon.forEach((coordinate: LinePolyline) => {
                    polygon.push(new window.google.maps.LatLng(coordinate.lat, coordinate.lng));
                });
                paths.push({name: line.name, color: line.color, polygon: polygon});
            });
            const that = this;
            paths.forEach((path) => {
                const polyline = this.$mapConfig.makePolyline(path);
                (this as any).polylines.push(polyline);
                polyline.addListener("click", () => {
                    const latLngBounds = new window.google.maps.LatLngBounds();
                    polyline.getPath().forEach((latLng: google.maps.LatLng) => {
                        latLngBounds.extend(latLng);
                    });
                    that.$mapConfig.map.fitBounds( latLngBounds ) ;
                });
            });
        },
        clearTime() {
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