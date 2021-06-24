<template>
    <div class="map-container">
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
// import practice from '~/assets/json/line/practice.json';
const tokyoBounds = {north: 35.860687,south: 35.530351, west: 138.9403931, east: 139.9368243}
interface Bounds {north: number, south: number, west: number, east: number};
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number,city_code: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string,stations: Station[]}
interface DataType {markerIcons: {jr: string,metro: string,toei: string, keio: string,tokyu: string},addMarker: { lat: number; lng: number; }[],map: google.maps.Map|null, overview: google.maps.Map|null, overviewConfig: {difference: number,maxZoom: number, minZoom: number},mapOptions: {center: google.maps.LatLng, restriction: {latLngBounds: Bounds, strictBounds: boolean,}, zoom: number,},markers: google.maps.Marker[][],polylines: google.maps.Polyline[],polygons: google.maps.Polygon[][]}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
export default Vue.extend({
    data(): DataType {
        return {
            map: null,
            overview: null,
            overviewConfig: {difference: 5,maxZoom: 13, minZoom: 3},
            mapOptions: {center: new google.maps.LatLng( 35.6729712, 139.7585771 ), restriction: {latLngBounds: tokyoBounds, strictBounds: false,}, zoom: 14,},
            markers: [],
            polylines: [],
            addMarker: [],
            polygons: [],
            markerIcons: {jr: require("~/assets/img/jr.png"),metro: require("~/assets/img/metro.png"),toei: require("~/assets/img/toei.png"),keio: require("~/assets/img/keio.png"),tokyu: require("~/assets/img/tokyu.png")},
        }
    },
    computed:{
        ...mapGetters('home', [
            'companies',
            'lines',
            'filteredLines',
            'bounds',
            'markerSwitch',
            'lineSwitch',
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
        },
    },
    mounted(){
        // this.$parent.$parent.$on('makePolyline',this.makeLineArray);
        const mapEl = this.$refs.map;
        let that = this;
        (this as any).map = new google.maps.Map(mapEl as HTMLElement, this.mapOptions);
        this.map?.addListener('click', (e: any)=>{this.addMarker.push({"lat": Math.round(e.latLng.lat()*1000000)/1000000, "lng": Math.round(e.latLng.lng()*1000000)/1000000});console.log({"lat": Math.round(e.latLng.lat()*1000000)/1000000, "lng": Math.round(e.latLng.lng()*1000000)/1000000});})
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
            this.onClickMap(e);
        })
        // new MarkerWithLabel({
        //     position: new google.maps.LatLng(35.6711584,139.6605155),
        //     map: this.map,
        //     labelContent: "foo", // can also be HTMLElement
        //     labelAnchor: new google.maps.Point(-21, 3),
        //     labelClass: "labels", // the CSS class for the label
        //     labelStyle: { opacity: 0 },
        //     // icon: {
        //     //     url: '',
        //     //     scaledSize: new google.maps.Size(32, 32)
        //     // },
        // })
    },
    methods:{
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
            // this.$store.dispatch('home/searchCityCode',e);
        },
        // isMarkerInPolygon(){//市町村毎にクラスターを作成する関数。非推奨
        //     const markers = this.markers.reduce((pre,current) => {pre.push(...current);return pre},[]);
        //     this.polygons.forEach((cityPolygons)=>{
        //         const sortedMarker = markers.filter((marker)=>{
        //             const latlng = marker.getPosition() as google.maps.LatLng;
        //             const isMarkerInPolygon = cityPolygons.some((polygon)=>{
        //                 return google.maps.geometry.poly.containsLocation(latlng, polygon);
        //             })
        //             return isMarkerInPolygon;
        //         })
        //         // sortedMarkers.push(sortedMarker);
        //         new MarkerClusterer(this.map, sortedMarker, {
        //             imagePath:
        //             "https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m",
        //         });
        //     })
        // },
        makePolygon(coordinates: {lat: number,lng: number}[], i: number){
            const polygon = new google.maps.Polygon({
                paths: coordinates,
                strokeColor: "red",
                strokeOpacity: 0.5,
                strokeWeight: 2,
                fillColor: "#FF9800",
                fillOpacity: 0.1,
            });
            const that = this;
            google.maps.event.addListener(polygon, 'click', function(e: google.maps.MapMouseEvent) {
                that.onClickMap(e);
            });
            polygon.setMap(this.map);
            return polygon
        },
        resetPoly(polygons: google.maps.Polygon[][]){
            polygons.forEach(cityPolygon => {
                cityPolygon.forEach(polygon => {
                    polygon.setMap(null)
                });
            });
        },
        // resetMapListeners(...arg: string[]){
        //     arg.forEach(event => {
        //         google.maps.event.clearListeners((this as any).map, event);
        //     });
        // },
        focusMarker(station: Station){
            (this as any).map.setZoom(16);
            const latLng = new google.maps.LatLng(station.lat, station.lng);
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
        async makeLineMarker(lines: Line[]){
            const markers: google.maps.Marker[][] = [];
            await lines.forEach((line: any,i: number)=>{
                const lineMarkerArray: google.maps.Marker[] = [];
                line.stations.forEach((station: Station)=>{
                    let marker = this.makeMarker(station);
                    marker.addListener("click", () => {
                        this.$store.dispatch('home/selectMarker',station);
                        // this.$store.dispatch('home/getStationInfo',{name: station.name});
                    });
                    lineMarkerArray.push(marker);
                });
                markers.push(lineMarkerArray)
            });
            const that = this;
            setTimeout(function(){
                that.$store.dispatch('home/resetMarkers',that.markers)
                .then(()=>{that.markers = markers;})
            },100)
        },
        makeMarker(station: Station){
            let img = '';
            // if (station.company_id == 1) {
            //     img = this.markerIcons.jr;
            // } else if(station.company_id == 7){
            //     img = this.markerIcons.tokyu;
            // } else if(station.company_id == 8){
            //     img = this.markerIcons.metro;
            // } else if(station.company_id == 9) {
            //     img = this.markerIcons.toei;
            // } else if(station.company_id == 2) {
            //     img = this.markerIcons.keio;
            // } else {
            //     img = ''
            // }
            const marker = new google.maps.Marker({
                map: this.map,
                position: new google.maps.LatLng(station.lat, station.lng),
                icon: img,
                // optimized: true,
            });
            return marker
        },
        makeLineArray(lines: Line[]){
            this.$store.dispatch('home/resetPolyline',this.polylines)
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
                    (that as any).map.fitBounds( latLngBounds ) ;
                });
            });
        },
        makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
            const polyline = new google.maps.Polyline({
                map: this.map,
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
    }
})
</script>

<style lang="scss" scoped>
.map-container{
    position:relative;
    width:100%;
    height:100vh;
    max-height:calc(100vh - 64px);
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
}
</style>