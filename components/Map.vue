<template>
    <div style="position:relative;width:100%;height:100vh;max-height:calc(100vh - 64px)">
        <div id="map" ref="map"></div>
        <div id="overview-wrapper">
            <div id="overview-container">
                <div id="overview" ref="overview"></div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
import { mapGetters } from 'vuex';
const tokyoBounds = {north: 35.860687,south: 35.530351, west: 138.9403931, east: 139.9368243}
interface Bounds {north: number, south: number, west: number, east: number};
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, pref_name: string, station_name: string, station_lat: number, station_lon: number, line_name: string, order: number, company_name: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, line_name: string, polygon: LinePolyline[], color: string,stations: Station[]}
interface DataType {map: google.maps.Map|null, overview: google.maps.Map|null, overviewConfig: {difference: number,maxZoom: number, minZoom: number},mapOptions: {center: google.maps.LatLng, restriction: {latLngBounds: Bounds, strictBounds: boolean,}, zoom: number,},markers: google.maps.Marker[][],polylines: google.maps.Polyline[]}
export default Vue.extend({
    data(): DataType {
        return {
            map: null,
            overview: null,
            overviewConfig: {difference: 5,maxZoom: 13, minZoom: 3},
            mapOptions: {center: new google.maps.LatLng( 35.6729712, 139.7585771 ), restriction: {latLngBounds: tokyoBounds, strictBounds: false,}, zoom: 14,},
            markers: [],
            polylines: [],
        }
    },
    watch:{
        lines(v){
            if (this.markerSwitch) {
                this.makeLineMarker(v);
            }
            if (this.lineSwitch) {
                this.makeLineArray(v);
            }
        },
        markerSwitch:{
            handler(){
                this.$store.dispatch('home/resetMarkers',this.markers)
                .then(()=>{
                    this.markers = [];
                    if (this.markerSwitch) {
                        this.makeLineMarker(this.lines);
                    }
                })
            },
            immediate: true,
        },
        lineSwitch:{
            handler(){
                this.$store.dispatch('home/resetPolyline',this.polylines)
                .then(()=>{
                    this.polylines = [];
                    if (this.lineSwitch) {
                        this.makeLineArray(this.lines);
                    }
                })
            },
            immediate: true
        },
        selectedMarker(v){
            this.focusMarker(v);
        }
    },
    computed:{
        ...mapGetters('home', [
            'lines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
            'stationInfo',
            'searchStations',
            'removeOverlap'
        ])
    },
    mounted(){
        // this.map?.addListener('click', (e: any)=>{this.addMarker.push({"lat": Math.round(e.latLng.lat()*1000000)/1000000, "lng": Math.round(e.latLng.lng()*1000000)/1000000})})
        this.$parent.$parent.$on('makePolyline',this.makeLineArray);
        const mapEl = this.$refs.map;
        let that = this;
        (this as any).map = new google.maps.Map(mapEl as HTMLElement, this.mapOptions);
        const overview = this.$refs.overview as HTMLElement;
        this.overview = new google.maps.Map(
             overview,
            {
                ...this.mapOptions,
                disableDefaultUI: true,
                gestureHandling: "none",
                zoomControl: false,
            }
        ) as any;
        let timer: NodeJS.Timer|null;
        (this as any).map.addListener("bounds_changed", () => {
            const bounds = this.culcCurrentBounds((this as any).map)
            const that = this;
            if(timer!==null){
                clearTimeout(timer)
            }
            timer = setTimeout(function(){that.$store.dispatch('home/getCurrentBounds', bounds);},1000);
            (that as any).overview.setCenter((that as any).map.getCenter());
            (that as any).overview.setZoom(
                (that as any).clamp(
                    (that as any).overview.getZoom() - this.overviewConfig.difference,
                    this.overviewConfig.minZoom,
                    this.overviewConfig.maxZoom
                )
            );
        });
        (this as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
            // that.clickMap(e);
        })
    },
    methods:{
        focusMarker(station: Station){
            (this as any).map.setZoom(16);
            const latLng = new google.maps.LatLng(station.station_lat, station.station_lon);
            (this as any).map.panTo(latLng);
        },
        culcCurrentBounds(map: google.maps.Map){
            const bounds = map.getBounds() as google.maps.LatLngBounds;
            const north = bounds.getNorthEast().lat();
            const south = bounds.getSouthWest().lat();
            const east = bounds.getNorthEast().lng();
            const west = bounds.getSouthWest().lng();
            return {south: south, north: north,east: east, west: west};
        },
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
        onClickResetPolyline(){
            this.$store.dispatch('resetPolyline', (this as any).polylines);
        },
        makeLineMarker(lines: Line[]){
            this.$store.dispatch('home/resetMarkers',this.markers)
            lines.forEach((line: any,i: number)=>{
                const lineMarkerArray: google.maps.Marker[] = [];
                line.stations.forEach((station: Station)=>{
                    let marker = this.makeMarker(station.station_lat, station.station_lon);
                    marker.addListener("click", () => {
                        this.$store.dispatch('home/selectMarker',station);
                        this.$store.dispatch('home/getStationInfo',{name: station.station_name});
                    });
                    lineMarkerArray.push(marker);
                })
                this.markers.push(lineMarkerArray);
            });
        },
        makeMarker(lat: number, lng: number){
            const marker = new google.maps.Marker({
                map: this.map,
                position: new google.maps.LatLng(lat, lng),
            });
            return marker
        },
        makeLineArray(lines: Line[]){
            this.$store.dispatch('home/resetPolyline',this.polylines)
            let paths: {color: string, polygon: google.maps.LatLng[]}[] = [];
            lines.forEach((line: Line)=>{
                let polygon: google.maps.LatLng[] = [];
                line.polygon.forEach((coordinate: LinePolyline)=>{
                    polygon.push(new google.maps.LatLng(coordinate.lat, coordinate.lng));
                });
                paths.push({color: line.color, polygon: polygon});
            });
            paths.forEach((path)=>{
                (this as any).makePolyline(path)
            });
        },
        makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
            const polyline = new google.maps.Polyline( {
                map: this.map,
                path:path.polygon,
                strokeColor: path.color,
                strokeOpacity: 0.9,
                strokeWeight: 4
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

<style lang="scss" scoped>
    #map {
        width: 100%;
        height: 100%;
        position: relative;
        // padding-top: 56.25%;
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
</style>