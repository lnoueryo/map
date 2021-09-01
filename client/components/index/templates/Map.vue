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
interface Polygon {lat: number, lng: number}
interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number, city_code: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface DataType {markers: {[key: string]: google.maps.Marker[][]}, polylines: google.maps.Polyline[], polygons: google.maps.Polygon[][], timer: null|NodeJS.Timer}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Cities   {code: string, province: string, lat: string, lng: string, city: string, spots: {name: string, place_id: string, address: string, lat: string, lng: string}}

export default Vue.extend({
    components: {
        LineChart,
        MapTop
    },
    data(): DataType {
        return {
            markers: {},
            polylines: [],
            polygons: [],
            timer: null
        }
    },
    computed: {
        ...mapGetters('home', [
            'lines',
            'cities',
            'selectedMarker',
            'selectedCompanyItems',
            'selectedCityItems',
            'selectedLineItems',
        ]),
        ...mapGetters('switch', [
            'fields',
            'markerSwitches',
            'markerSwitch',
            'lineSwitch',
            'chartSwitch',
            'dotSwitch',
        ])
    },
    watch: {
        markerSwitches: {
            handler(v) {
                console.log(v)
                this.showMarkers()
            },
            deep: true
        },
        'markerSwitches.stations': {
            handler(v) {
                if(!v) {
                    if (this.selectedCompanyItems.length !== 0) {
                        this.$store.dispatch('home/selectedCompanyItems', []);
                    }
                    if (this.selectedLineItems.length !== 0) {
                        this.$store.dispatch('home/selectedLineItems', []);
                    }
                }
            }
        },
        selectedCompanyItems: {
            async handler() {
                if (this.markerSwitch) {
                    this.$mapConfig.resetMarkers(this.markers.stations);
                    this.markers.stations = [];
                    this.markers.stations = await this.$mapConfig.makeMarkers(this.lines, 'stations', this.stationMarkerFunction);
                    this.showMarkers();
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
                    this.$mapConfig.resetMarkers(this.markers.stations);
                    this.markers.stations = [];
                    this.markers.stations = await this.$mapConfig.makeMarkers(this.lines, 'stations', this.stationMarkerFunction);
                    this.showMarkers();
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
                this.makeCityPolygon(v);
            },
        },
        markerSwitch: {
            handler(value) {
                if(value) {
                    this.showMarkers();
                } else {
                    this.$mapConfig.hideMarkers(this.markers.stations);
                    this.$mapConfig.hideMarkers(this.markers.spots);
                }
            }
        },
        lineSwitch: {
            handler(value) {
                value ? this.makeLineArray(this.lines) : this.$mapConfig.resetPolyline(this.polylines);
            }
        },
        selectedMarker: {
            handler(v) {
                const zoom = 16;
                this.$mapConfig.focusMarker(v, zoom);
            }
        },
    },
    beforeCreate() {
        this.$store.dispatch('switch/makeSwitches');
    },
    created() {
        this.fields.forEach((field: string) => {
            this.markers[field] = [];
        });
    },
    async mounted() {
        await this.setMap();
        this.setMarkers();
        let timer: NodeJS.Timer|null;

        this.$mapConfig.map.addListener("bounds_changed", () => {
            const bounds = this.$mapConfig.currentBounds();
            const getMapCenter = this.$mapConfig.map.getCenter();
            const mapCenter = {lat: getMapCenter.lat(), lng: getMapCenter.lng()};
            const zoom = this.$mapConfig.map.getZoom();
            console.log(zoom);
            if(timer !== null) clearTimeout(timer)
            timer = setTimeout(() => {
                this.showMarkers();
                this.$store.dispatch('home/getCity', {mapCenter: mapCenter, zoom: zoom});
                this.$store.dispatch('home/getCurrentBounds', bounds);
            }, 1000);
            zoom > 13 ? this.$mapConfig.changeIcon(this.markers.stations, 'stations', 'big') : this.$mapConfig.changeIcon(this.markers.stations, 'stations', 'small');
            // zoom > 13 ? this.$mapConfig.changeIcon(this.markers.spots, 'spots', 'big') : this.$mapConfig.changeIcon(this.markers.spots, 'spots', 'small');
        });
    },
    methods:{
        async setMap() {
            const mapEl = this.$refs.map;
            this.$mapConfig.makeMap(mapEl as HTMLElement);
            this.addClickMapListeners();
        },
        async setMarkers() {
            this.markers.stations = await this.$mapConfig.makeMarkers(this.lines, 'stations', this.stationMarkerFunction);
            this.markers.cities = await this.$mapConfig.makeMarkers([{cities: this.cities}], 'cities', this.cityMarkerFunction);
            // this.markers.spots = await this.$mapConfig.makeMarkers(this.cities, 'spots', this.spotMarkerFunction)
        },
        showMarkers() {
            if(this.markerSwitch) {
                this.fields.forEach((field: string) => {
                    const markers = this.$mapConfig.boundsFilterForMarker(this.markers[field], this.markerSwitches[field]) as any;
                    this.$mapConfig.cityFilterForMarker(markers, this.polygons, this.selectedCityItems);
                });
            }
        },
        stationMarkerFunction(marker: google.maps.Marker, station: {name: string}) {
            marker.addListener("click", async () => {
                this.$store.dispatch('home/selectMarker',station);
                this.$store.commit('info/twitterInfo', []);
                this.$store.dispatch('info/getTwitterInfo', {name: station.name});
                await this.$store.dispatch('info/getStationInfo', {name: station.name});
                this.$store.commit('info/searching', false);

            });
        },
        cityMarkerFunction(marker: google.maps.Marker, city: {name: string}) {
                marker.addListener("click", async (e: google.maps.MapMouseEvent) => {
                    await this.$store.dispatch('home/searchCityCode', e);
                    // this.$store.dispatch('home/selectMarker', word);
                    // await this.$store.dispatch('info/getTwitterInfo', {name: word.name});
                    // this.$store.commit('info/searching', false)
                });
        },
        spotMarkerFunction(marker: google.maps.Marker, spot: {name: string}) {
            marker.addListener("click", async () => {
                this.$store.dispatch('home/selectMarker', spot);
                this.$store.dispatch('info/getTwitterInfo', {name: spot.name});
                await this.$store.dispatch('info/getStationInfo', {name: spot.name})
                // this.$store.commit('info/searching', false)
            });
            this.$mapConfig.createInfoWindow(marker, spot.name);
        },
        makeCityPolygon(v: City[]) {
            const that = this;
            const polygons = v.map((selectedCityItem: City, index: number) => {
                return selectedCityItem.polygons.map((polygon_obj) => {
                    const polygon = this.$mapConfig.makePolygon(polygon_obj, index);
                    window.google.maps.event.addListener(polygon, 'click', (e: google.maps.MapMouseEvent) => {
                        that.onClickMap(e);
                    });
                    return polygon;
                })
            })
            if (this.polygons.length !== 0) {
                this.$mapConfig.resetPolygon(this.polygons);
            }
            this.polygons = polygons;
            this.showMarkers();
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
                this.clearTime();
                const that = this;
                this.timer = setTimeout(() => {
                    that.onClickMap(e);
                },360);
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
            if (this.timer) clearTimeout(this.timer);
        }
    }
})
</script>

<style lang="scss" scoped>

.map-container {
    position: relative;
    width: 100%;
    height: 100vh;
    max-height: calc(100vh - 64px);
    .line-chart {
        position: absolute;
        top: 40px;
        bottom: 0;
        right: 0;
        left: 0;
        margin: auto;
    }
    .map-top {
        position: absolute;
        z-index: 1;
    }
    .dot {
        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;
        margin: auto;
        width: 9px;
        height: 9px;
        border-radius:50%;
        background-color: red;
        opacity: 0.4;
        transition: all 2s;
    }
    #map {
        width: 100%;
        height: 100%;
        position: relative;
        // padding-top: 56.25%;
        transition: all .5s
    }
    .show-line {
        opacity: 0.4;
    }
    #overview-wrapper {
        position: absolute;
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
            content: "";
            display: block;
            padding-top: 56.25%;
        }
    }
    @media screen and (max-width: 500px) {
        .map-top {
            top: 50px;
        }
        .line-chart{
            top: 100px;
        }
    }

}
</style>