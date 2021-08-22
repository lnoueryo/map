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
interface DataType {stationIcon: {small: string, big: string}, spotIcon: {small: string, big: string},stationMarkers: google.maps.Marker[][],cityMarkers: google.maps.Marker[][],spotMarkers: google.maps.Marker[][],polylines: google.maps.Polyline[],polygons: google.maps.Polygon[][],timer: null|NodeJS.Timer}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Words   {code: string, province: string, lat: string, lng: string, city: string, spots: {name: string, place_id: string, address: string, lat: string, lng: string}}

export default Vue.extend({
    components: {
        LineChart,
        MapTop
    },
    data(): DataType {
        return {
            stationIcon: {small: require('~/assets/img/train.png'), big: require('~/assets/img/station.png')},
            spotIcon: {small: require('~/assets/img/spot_small.png'), big: require('~/assets/img/spot.png')},
            stationMarkers: [],
            cityMarkers: [],
            spotMarkers: [],
            polylines: [],
            polygons: [],
            timer: null
        }
    },
    computed:{
        ...mapGetters('home', [
            'lines',
            'words',
            'events',
            'markerSwitch',
            'lineSwitch',
            'chartSwitch',
            'dotSwitch',
            'selectedMarker',
            'selectedCompanyItems',
            'selectedCityItems',
            'selectedLineItems',
            'stationSwitch',
            'citySwitch',
            'spotSwitch',
        ])
    },
    watch:{
        stationSwitch: {
            handler(v) {
                this.showMarkers()
                if(!v) {
                    this.$store.dispatch('home/selectedCompanyItems', [])
                    this.$store.dispatch('home/selectedLineItems', []);
                }
            }
        },
        spotSwitch: {
            handler() {
                this.showMarkers()
            }
        },
        selectedCompanyItems: {
            async handler() {
                if (this.markerSwitch) {
                    this.$mapConfig.resetMarkers(this.stationMarkers);
                    this.stationMarkers = [];
                    await this.makeStationMarker(this.lines)
                    this.showMarkers()
                }
                if (this.lineSwitch) {
                    this.$mapConfig.resetPolyline(this.polylines);
                    this.polylines = [];
                    this.makeLineArray(this.lines);
                }
            },
        },
        selectedLineItems: {
            async handler(v) {
                if (this.markerSwitch) {
                    this.$mapConfig.resetMarkers(this.stationMarkers);
                    this.stationMarkers = [];
                    await this.makeStationMarker(this.lines)
                    this.showMarkers()
                }
                if (this.lineSwitch) {
                    this.$mapConfig.resetPolyline(this.polylines);
                    this.polylines = [];
                    this.makeLineArray(this.lines);
                }
            },
        },
        selectedCityItems: {
            handler(v){
                this.makeCityPolygon(v)
            },
        },
        markerSwitch:{
            handler(value){
                if (value) {
                    this.showMarkers()
                } else {
                    this.$mapConfig.hideMarkers(this.stationMarkers)
                    this.$mapConfig.hideMarkers(this.spotMarkers)
                }
            },
            immediate: false,
        },
        lineSwitch:{
            handler(value){
                value ? this.makeLineArray(this.lines) : this.$mapConfig.resetPolyline(this.polylines)
            },
            immediate: false
        },
        selectedMarker: {
            handler(v) {
                const zoom = 16
                this.$mapConfig.focusMarker(v, zoom);
            }
        },
    },
    async mounted(){
        await this.setMap()
        let timer: NodeJS.Timer|null;
        this.addClickMapListeners()
        this.makeStationMarker(this.lines)
        this.makeCityMarkers(this.words)
        this.makeSpotMarkers(this.words)
        this.$mapConfig.map.addListener("bounds_changed", () => {
            const bounds = this.$mapConfig.currentBounds()
            const getMapCenter = this.$mapConfig.map.getCenter();
            const mapCenter = {lat: getMapCenter.lat(), lng: getMapCenter.lng()};
            const zoom = this.$mapConfig.map.getZoom();
            console.log(zoom)
            if(timer !== null) {
                clearTimeout(timer)
            }
            timer = setTimeout(() => {
                this.showMarkers()
                this.$store.dispatch('home/getCity', {mapCenter: mapCenter, zoom: zoom});
                this.$store.dispatch('home/getCurrentBounds', bounds);
            },500);
            zoom > 13 ? this.$mapConfig.changeIcon(this.stationMarkers, this.stationIcon.big) : this.$mapConfig.changeIcon(this.stationMarkers, this.stationIcon.small);
            zoom > 13 ? this.$mapConfig.changeIcon(this.spotMarkers, this.spotIcon.big) : this.$mapConfig.changeIcon(this.spotMarkers, this.spotIcon.small);
        });
    },
    methods:{
        async setMap() {
            const mapEl = this.$refs.map;
            this.$mapConfig.makeMap(mapEl as HTMLElement)
        },
        showMarkers() {
            const stationMarkers = this.$mapConfig.boundsFilterForMarker(this.stationMarkers, this.stationSwitch) as any;
            this.$mapConfig.cityFilterForMarker(stationMarkers, this.polygons, this.selectedCityItems);
            const spotMarkers = this.$mapConfig.boundsFilterForMarker(this.spotMarkers, this.spotSwitch) as any;
            this.$mapConfig.cityFilterForMarker(spotMarkers, this.polygons, this.selectedCityItems);
            const cityMarkers = this.$mapConfig.boundsFilterForMarker(this.cityMarkers, this.citySwitch) as any;
            this.$mapConfig.cityFilterForMarker(cityMarkers, this.polygons, this.selectedCityItems);
        },
        async makeStationMarker(lines: Line[]) {
            const zoom = this.$mapConfig.map.getZoom();
            const icon = (zoom > 13) ? this.stationIcon.big : this.stationIcon.small
            const markers: google.maps.Marker[][] = [];
            await lines.forEach((line: any,i: number) => {
                const lineMarkerArray: google.maps.Marker[] = [];
                line.stations.forEach((station: Station) => {
                    let marker = this.$mapConfig.makeMarker(station, icon);
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
            this.stationMarkers = markers;
        },
        async makeCityMarkers(words: Words[]) {
            const markers: google.maps.Marker[][] = [];
            await words.forEach((word: any, i: number) => {
                let marker = this.$mapConfig.makeMarker(word, '');
                marker.addListener("click", async () => {
                    // this.$store.dispatch('home/selectMarker', word);
                    // await this.$store.dispatch('home/getTwitterInfo', {name: word.name});
                    // this.$store.commit('home/searching', false)
                });
                markers.push([marker]);
            });
            this.cityMarkers = markers
        },
        async makeSpotMarkers(words: Words[]) {
            const markers: google.maps.Marker[][] = [];
            await words.forEach((word: any, i: number) => {
                const spotMarkerArray: google.maps.Marker[] = [];
                word.spots.forEach((spot: Station) => {
                    let marker = this.$mapConfig.makeMarker(spot, this.spotIcon.big, spot.name);
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
            this.spotMarkers = markers
        },
        makeCityPolygon(v: City[]) {
            const that = this;
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
            this.polygons = polygons;
            this.showMarkers()
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
        makeLineArray(lines: Line[]) {
            if(this.selectedLineItems.length !== 0 || this.selectedCompanyItems.length !== 0 ) {
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
            }
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