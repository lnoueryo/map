<template>
    <div>
        <div id="container">
            <div id="map" ref="map"></div>
            <div id="overview-wrapper">
                <div id="overview-container">
                    <div id="overview" ref="overview"></div>
                </div>
            </div>
            <v-btn color="success" @click="back">back</v-btn>
            <v-btn color="success" @click="next">next</v-btn>
            <v-btn color="success" @click="allPolygons(polygons)">allPolygons</v-btn>
            <v-btn color="success" @click="resetPolygons(polygons)">resetPolygons</v-btn>
            <v-btn color="success" @click="refresh">refresh</v-btn>
        </div>
        <line-chart></line-chart>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import LineChart from '../components/LineChart.vue'
import polygonData from '~/assets/json/coordinates.json'
interface Polygons {"code":string,"city":string,"polygons":Polygon[][]}
interface Polygon {"lat":number,"lng":number}
interface DataType {
    map: google.maps.Map | null,
    overview: google.maps.Map | null,
    index: number,
    polygon: google.maps.Polygon[] | null,
    polygons: google.maps.Polygon[][],
}
export default Vue.extend({
    components: {
        LineChart
    },
    data(): DataType {
        return {
            map: null,
            overview: null,
            index: 0,
            polygon: null,
            polygons: [],
        }
    },
    mounted(){
        const OVERVIEW_DIFFERENCE = 5;
        const OVERVIEW_MIN_ZOOM = 3;
        const OVERVIEW_MAX_ZOOM = 13;
        const TOKYO_BOUNDS = {
        north: 35.860687,
        south: 35.5543518,
        west:  138.9403931,
        east:139.9368243,
        };
        const mapOptions = {
            center: { lat: 35.6729712, lng: 139.7585771 },
            restriction: {
                latLngBounds: TOKYO_BOUNDS,
                strictBounds: false,
            },
            zoom: 12,
        }
        this.map = new google.maps.Map(this.$refs.map as HTMLElement, {
            ...mapOptions,
        }) as any;
        const overview = this.$refs.overview as HTMLElement;
        this.overview = new google.maps.Map(
             overview,
            {
            ...mapOptions,
            disableDefaultUI: true,
            gestureHandling: "none",
            zoomControl: false,
            }
        ) as any;
        this.currentPosition();

        const that = this;
        (this as any).map.addListener("bounds_changed", () => {
            (that as any).overview.setCenter((that as any).map.getCenter());
            (that as any).overview.setZoom(
                that.clamp(
                    (that as any).overview.getZoom() - OVERVIEW_DIFFERENCE,
                    OVERVIEW_MIN_ZOOM,
                    OVERVIEW_MAX_ZOOM
                )
            );
        });
        (this as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
            that.clickMap(e);
        })
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
            strokeWeight: 2,
        });

        flightPath.setMap(this.map);
        this.setPolygons()
    },
    methods:{
        async refresh(){
            const token = localStorage.getItem('token');
            const parsedToken = JSON.parse(token as string)
            const response = await this.$axios.$post('/api/token/refresh/', {refresh: parsedToken.refresh});
            this.$axios.setToken(response.access, 'Bearer')
            console.log(response)
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
                        that.resetPoly(i)
                        // that.designatePolygon(i)
                    });
                    polygons.push(polygon);
                });
                this.polygons.push(polygons as never)
            })
        },
        async clickMap(e: google.maps.MapMouseEvent){
            this.resetMapListeners('click')
            const latLng = {lat: e.latLng?.lat(), lng: e.latLng?.lng()};
            const response = await this.$axios.$post('/api/map/search-by-reverse-geocode', latLng as any);
            polygonData.forEach((city: Polygons, i: number) => {
                if (city.city == response.Property.AddressElement[1].Name) {
                    this.makePolygon(i)
                }
            });
            const that = this;
            setTimeout(()=>{
                (that as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
                    that.clickMap(e)
                })
            },1500)
        },
        allPolygons(polygons: google.maps.Polygon[][]){
            this.resetPolygons(polygons)
            polygons.forEach((polygon: google.maps.Polygon[]) => {
                polygon.forEach((coordinates) => {
                    coordinates.setMap(this.map)
                });
            });
        },
        resetPolygons(polygons: google.maps.Polygon[][]){
            polygons.forEach(polygon => {
                polygon.forEach(coordinates => {
                    coordinates.setMap(null)
                });
            });
        },
        makePolygon(index: number){
            const polygons: google.maps.Polygon[] = this.polygons[index]
            polygons.forEach((polygon) => {
                polygon.addListener("click", () => {
                    this.resetPoly(index)
                });
                polygon.setMap(this.map);
            });
        },
        resetPoly(index: number){
            const polygons: google.maps.Polygon[] = this.polygons[index]
            polygons.forEach(polygon => {
                polygon.setMap(null)
            });
        },
        next(){
            this.index +=1
            this.resetPoly(this.index)
            this.makePolygon(this.index)
        },
        back(){
            this.index -=1
            this.resetPoly(this.index)
            this.makePolygon(this.index)
        },
        clamp(num: number, min: number, max: number) {
          return Math.min(Math.max(num, min), max);
        },
        resetMapListeners(...arg: string[]){
            arg.forEach(event => {
                google.maps.event.clearListeners((this as any).map, event);
            });
        },
        currentPosition(){
            const infoWindow = new google.maps.InfoWindow();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const coordinate = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude,
                        };
                        const marker = new google.maps.Marker({
                            position: coordinate,
                            map: this.map,
                        });
                        // infoWindow.setPosition(coordinate);
                        // infoWindow.setContent("Location found.");
                        // infoWindow.open(this.map);a
                        (this as any).map.panTo(coordinate);
                    },
                    () => {
                        console.log('hello')
                    // handleLocationError(true, infoWindow, map.getCenter()!);
                    }
                );
            } else {
                // handleLocationError(false, infoWindow, map.getCenter()!);
            }
        }
    }
})
</script>

<style>
        #map {
            height: 100%;
            position: relative;
            padding-top: 56.25%;
        }
        #container {
            height: 100%;
            width: 100%;
            position:relative
        }
        #overview-wrapper{
            position:absolute;
            width: 30%;
            bottom: 50px;
            left: 15px;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
        }
        #overview-container {
            position: relative;
            width: 100%;
        }
        #overview-container:before {
            content:"";
            display: block;
            padding-top: 56.25%; /* 高さと幅の比を16:9に固定。9/16*100=56.25 */
        }
        #overview {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
</style>