<template>
    <div class="d-flex" style="width:100%">
        <div style="width:300px">
            <div style="padding:9px"><div><span>lat:{{currentMarker.lat}}</span></div><div><span>lng:{{currentMarker.lng}}</span></div></div>
            <textarea v-if="index==0" name="" id="" cols="30" rows="40" v-html="replace" style="width:100%;background-color:white;font-size:12px;word-break:break-all;"></textarea>
            <textarea v-if="index==1" @input="makePolyline(polylineJSON)" cols="30" rows="40" v-model="polylineJSON" style="width:100%;background-color:white;font-size:12px;word-break:break-all;"></textarea>
        </div>
        <div class="map-container">
            <v-btn @click="index--" absolute top left style="z-index:1;">back</v-btn>
            <v-btn @click="index++" absolute top style="z-index:1;left:100px">next</v-btn>
            <div id="map" ref="map"></div>
        </div>
        <v-dialog v-model="loading" hide-overlay width="300" style="z-index:10000">
            <v-card color="primary" dark style="z-index:10000">
                <v-card-text>
                Please stand by
                <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                </v-card-text>
            </v-card>
        </v-dialog>
        <!-- <div style="position:fixed;top:0;bottom:0;right:0;left:0;z-index:100;"></div> -->
    </div>
</template>

<script>
const tokyoBounds = {north: 35.860687,south: 35.530351, west: 138.9403931, east: 139.9368243}
export default {
    data() {
        return {
            map: null,
            mapOptions: {center: new google.maps.LatLng( 35.6729712, 139.7585771 ), restriction: {latLngBounds: tokyoBounds, strictBounds: false,}, zoom: 14,},
            coordinates: [],
            autoIncrement: 0,
            index: 0,
            currentMarker: {},
            markers: [],
            polyline: null,
            polylineJSON: [],
            exponentialBackoff: 1000,
            loading: false,
        }
    },
    computed:{
        replace(){
            const coordinates = JSON.parse(JSON.stringify(this.coordinates))
            return JSON.stringify(coordinates.map((marker)=>{delete marker.index;return marker})).replace(/\s+/g,'')
        }
    },
    watch:{
        polylineJSON(value){
            if (!value) {
                this.polylineJSON = []
            }
        }
    },
    mounted(){
        const mapEl = this.$refs.map;
        this.map = new google.maps.Map(mapEl, this.mapOptions);
        (this).map.addListener('click', (e)=>{
            this.clickMap(e);
        })
    },
    methods:{
        clickMap(e){
            const lat = (e.latLng).lat();
            const lng = (e.latLng).lng();
            const latLng = {"lat": Math.round(lat*1000000)/1000000, "lng": Math.round(lng*1000000)/1000000, index: this.autoIncrement};
            this.coordinates.push(latLng);
            this.makeMarker(lat,lng)
            this.currentMarker = Object.assign({}, this.currentMarker, latLng)
            this.autoIncrement++;
            if (this.polyline) {
                this.polyline.setMap(null);
            }
            this.polyline = new google.maps.Polyline( {
                map: this.map ,
                path: this.coordinates,
                strokeWeight: 3,
            });
        },
        makeMarker(lat,lng){
            const marker = new google.maps.Marker({
                map: this.map,
                position: new google.maps.LatLng(lat, lng),
            });
            let index = JSON.parse(JSON.stringify(this.autoIncrement));
            marker.addListener("click", () => {
                marker.setMap(null);
                this.coordinates = this.coordinates.filter((marker)=>{
                    return marker.index !== index;
                })
            });
        },
        makePolyline(value){
            this.loading=true;
            try {
                if (this.polyline) {
                    this.polyline.setMap(null)
                }
                if (value) {
                    this.polyline = new google.maps.Polyline({
                        map: this.map,
                        path:JSON.parse(value),
                        strokeColor: 'red',
                        strokeOpacity: 0.9,
                        strokeWeight: 3,
                        geodesic: true ,
                    });
                }
                this.exponentialBackoff = 1000;
                this.loading = false;
            } catch (error) {
                const pow = 2;
                this.exponentialBackoff = this.exponentialBackoff*pow;
                const that = this;
                let timer = setTimeout(function(){that.makePolyline(value)},that.exponentialBackoff);
                if(this.exponentialBackoff>=16000){
                    clearInterval(timer);
                    alert('json形式で入れてください');
                    this.loading=false;
                    this.polylineJSON = [];
                    this.exponentialBackoff = 1000;
                }
            }
        },
    }
}
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
        padding-top: 56.25%;
    }
}
</style>