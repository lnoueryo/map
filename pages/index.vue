<template>
    <div>
        <div id="container">
            <div id="map" ref="map"></div>
            <!-- <div id="overview-wrapper">
                <div id="overview-container">
                    <div id="overview" ref="overview"></div>
                </div>
            </div> -->
            <v-btn color="success" @click="back">back</v-btn>
            <v-btn color="success" @click="next">next</v-btn>
            <v-btn color="success" @click="allPolygons(polygons)">allPolygons</v-btn>
            <v-btn color="success" @click="resetPolygons(polygons)">resetPolygons</v-btn>
            <v-btn color="success" @click="refresh">refresh</v-btn>
            <!-- <v-btn color="success" @click="makeStationsMarkers">showMarkers</v-btn> -->
            <v-btn color="success" @click="check">check</v-btn>
            <!-- <v-btn color="success" @click="markerPosition">markerPosition</v-btn> -->
            <v-btn color="success" @click="makeLineArray">makeLineArray</v-btn>
            <v-btn color="success" @click="makeLineMarker">makeLineMarker</v-btn>
        </div>
        <line-chart></line-chart>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import LineChart from '../components/LineChart.vue'
import ItemSelect from '../components/ItemSelect.vue'
import polygonData from '~/assets/json/coordinates.json'
import practice from '~/assets/json/line/practice.json'
import Mixin from '~/utils/mixin.ts'
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface Station {id: number, pref_name: string, station_name: string, station_lat: number, station_lon: number, line_name: string, order: number, company_name: string}
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, line_name: string, polygon: LinePolyline[], color: string}
interface DataType {
    addMarker: LinePolyline[]
    map: google.maps.Map | null,
    overview: google.maps.Map | null,
    index: number,
    polygon: google.maps.Polygon[] | null,
    polygons: google.maps.Polygon[][],
    stations: LinePolyline[],
    markers: google.maps.Marker[],
    lines: Line[]
}
export default Vue.extend({
    mixins: [Mixin],
    components: {
        LineChart,
        ItemSelect
    },
    data(): DataType {
        return {
            addMarker: [],
            map: null,
            overview: null,
            index: 0,
            polygon: null,
            polygons: [],
            stations: [],
            markers: [],
            lines: []
        }
    },
    async created(){
        const response = await this.$axios.$get('/api/map/station/polygon/');
        this.lines = response;
    },
    mounted(){
        this.$axios.$get('/api/map/station/line/').then((res)=>{this.stations = res;})
        const OVERVIEW_DIFFERENCE = 5;
        const OVERVIEW_MIN_ZOOM = 3;
        const OVERVIEW_MAX_ZOOM = 13;
        const TOKYO_BOUNDS = {
            north: 35.860687,
            south: 35.530351,
            west: 138.9403931,
            east: 139.9368243,
        };
        const mapOptions = {
            center: new google.maps.LatLng( 35.6729712, 139.7585771 ),
            restriction: {
                latLngBounds: TOKYO_BOUNDS,
                strictBounds: false,
            },
            zoom: 12,
        }
        this.map = new google.maps.Map(this.$refs.map as HTMLElement, {
            ...mapOptions,
        }) as any;
        let that = this;
        this.map?.addListener('click', (e: any)=>{this.addMarker.push({"lat": Math.round(e.latLng.lat()*1000000)/1000000, "lng": Math.round(e.latLng.lng()*1000000)/1000000})})
        const overview = this.$refs.overview as HTMLElement;
        // this.overview = new google.maps.Map(
        //      overview,
        //     {
        //     ...mapOptions,
        //     disableDefaultUI: true,
        //     gestureHandling: "none",
        //     zoomControl: false,
        //     }
        // ) as any;
        // (this as InstanceType<typeof Mixin>).currentPosition();

        // const that = this;
        (this as any).map.addListener("bounds_changed", () => {
            (that as any).overview.setCenter((that as any).map.getCenter());
            (that as any).overview.setZoom(
                (that as InstanceType<typeof Mixin>).clamp(
                    (that as any).overview.getZoom() - OVERVIEW_DIFFERENCE,
                    OVERVIEW_MIN_ZOOM,
                    OVERVIEW_MAX_ZOOM
                )
            );
        });
        // (this as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
        //     that.clickMap(e);
        // })
        const flightPlanCoordinates = [
            { lat: 37.772, lng: -122.214 },
            { lat: 21.291, lng: -157.821 },
            { lat: -18.142, lng: 178.431 },
            { lat: -27.467, lng: 153.027 },
        ];
        const flightPath = new google.maps.Polyline({
            path: flightPlanCoordinates,
            geodesic: true,
            strokeColor: "#FF0000",
            strokeOpacity: 1.0,
            strokeWeight: 3,
        });

        flightPath.setMap(this.map);
        this.setPolygons()
        const latLngBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(35.554351, 138.9403931) ,
            new google.maps.LatLng(35.860687, 139.9368243)
        );
        // this.makeLineMarker()
    },
    methods:{
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
            this.lines.forEach((line: Line)=>{
                let polygon: google.maps.LatLng[] = []
                line.polygon.forEach((coordinate: LinePolyline)=>{
                    polygon.push(new google.maps.LatLng(coordinate.lat, coordinate.lng))
                })
                paths.push({color: line.color, polygon: polygon})
            })
            paths.forEach((path)=>{
                this.makePolyline(path)
            })
        },
        makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
            const polyline = new google.maps.Polyline( {
                map: this.map,
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
            const TOKYO_BOUNDS = {
                north: 35.760687,
                south: 35.530351,
                west: 139.2403931,
                east: 139.9368243,
            };
            (this as any).map.fitBounds( TOKYO_BOUNDS );
        },
        markerPosition(){
            // console.log(this.markers[0].setPosition(new google.maps.LatLng( 35.6666601740126, 139.35275529999995 )))
            // console.log(this.markers[0].position.lat.lat())
        },
        async check(){
            const bounds = (this as any).map.getBounds()
            console.log(bounds)
            const north = bounds.getNorthEast().lat();
            const south = bounds.getSouthWest().lat();
            const east = bounds.getNorthEast().lng();
            console.log(east)
            const west = bounds.getSouthWest().lng();
            const paramater = {params: {line_name: 'ＪＲ中央本線(東京－塩尻)',south: south, north: north,east: east, west: west}}
            const response = await this.$axios.$get('/api/map/station/line/', paramater);
            this.makeStationsMarkers(response)
        },
        makeStationsMarkers(stations: Station[]){
            stations.forEach((station)=>{
                const marker = (this as InstanceType<typeof Mixin>).makeMarker(station.station_lat, station.station_lon);
                this.markers.push(marker)
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
                this.polygons.push(polygons as never)
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
                    that.clickMap(e)
                })
            },1500)
        },
        next(){
            this.index +=1 as any
            (this as InstanceType<typeof Mixin>).resetPoly(this.index)
            (this as InstanceType<typeof Mixin>).makePolygon(this.index)
        },
        back(){
            this.index -=1 as any
            (this as InstanceType<typeof Mixin>).resetPoly(this.index)
            (this as InstanceType<typeof Mixin>).makePolygon(this.index)
        },
    }
})
</script>

<style lang="scss">
    #container {
        height: 100%;
        width: 100%;
        position:relative;
        #map {
            height: 100%;
            position: relative;
            padding-top: 56.25%;
        }
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