<template>
    <div>
        {{mapa}}
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
export default Vue.extend({
    data() {
        return {
            map: null,
            overview: null
        }
    },
    computed:{
        mapa(){
            return this.$store.state.map;
        }
    },
    mounted(){
        const mapEl = this.$refs.map;
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

        let that = this;
        (this as any).map = new google.maps.Map(mapEl as HTMLElement, {
            ...mapOptions,
        });
        // this.$store.state.map = String(map)
        this.$store.commit('map', this.map)
        // (this as any).map = new google.maps.Map(mapEl as HTMLElement, {
        //     ...mapOptions,
        // });
        // this.map?.addListener('click', (e: any)=>{this.addMarker.push({"lat": Math.round(e.latLng.lat()*1000000)/1000000, "lng": Math.round(e.latLng.lng()*1000000)/1000000})})
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

        (this as any).map.addListener("bounds_changed", () => {
            (that as any).overview.setCenter((that as any).map.getCenter());
            (that as any).overview.setZoom(
                (that as any).clamp(
                    (that as any).overview.getZoom() - OVERVIEW_DIFFERENCE,
                    OVERVIEW_MIN_ZOOM,
                    OVERVIEW_MAX_ZOOM
                )
            );
        });
        (this as any).map.addListener('click', (e: google.maps.MapMouseEvent)=>{
            // that.clickMap(e);
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
            strokeWeight: 3,
        });

        flightPath.setMap((this as any).map);
        const latLngBounds = new google.maps.LatLngBounds(
            new google.maps.LatLng(35.554351, 138.9403931) ,
            new google.maps.LatLng(35.860687, 139.9368243)
        );
    },
    methods:{
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
    }
})
</script>

<style lang="scss" scoped>
    #map {
        height: 100%;
        position: relative;
        padding-top: 56.25%;
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