<template>
    <div class="d-flex" style="width:100%">
        <div style="width:340px">
            <div style="padding:9px"><div><span>lat:{{currentMarker.lat}}</span>　<span>lng:{{currentMarker.lng}}</span></div></div>
            <v-btn @click="resetAll">リセット</v-btn>
            <textarea ref="polyline" cols="30" rows="40" @input="onChangeText" style="width:100%;background-color:white;font-size:12px;word-break:break-all;"></textarea>
        </div>
        <div class="map-container">
            <div id="map" ref="map"></div>
            <div style="position:absolute;top:0;bottom:0;right:0;left:0;z-index:100;" v-if="loading">
            <v-card color="primary" dark style="position:absolute;width:250px;height:60px;bottom:0;top:0;margin:auto;right:0;left:0;">
                <v-card-text>
                Please stand by
                <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                </v-card-text>
            </v-card>
            </div>
        </div>
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
            currentMarker: {},
            markers: [],
            polyline: null,
            polygon: [],
            polylineJSON: [],
            exponentialBackoff: 1000,
            loading: false,
        }
    },
    watch:{
        coordinates(){
            if(this.coordinates){
                const coordinates = JSON.parse(JSON.stringify(this.coordinates))
                this.$refs.polyline.value = JSON.stringify(coordinates.map((marker)=>{delete marker.index;return marker})).replace(/\s+/g,'');
            }
        }
    },
    mounted(){
        const mapEl = this.$refs.map;
        this.map = new google.maps.Map(mapEl, this.mapOptions);
        (this).map.addListener('click', (e)=>{
            this.onClickMap(e);
        })
    },
    methods:{
        onClickMap(e){
            const latLng = this.makeLatLng(e, this.autoIncrement); //クリックしたところの緯度経度及びindexを算出 {lat: '', lng: '', index: ''}
            this.coordinates.push(latLng); //{lat: '', lng: '', index: ''}をデータに格納
            const marker = this.makeMarker(latLng, this.autoIncrement); //
            this.markers.push(marker);
            this.makePolylinePush(this.coordinates)//this.coordinatesはlatLng[] この処理を最後にしないと処理がおかしくなる
            this.currentMarker = Object.assign({}, this.currentMarker, latLng); //現在の緯度経度を表示
            this.autoIncrement++;//次のindexのために+1
        },
        onDragMarker(e, index){
            const latLng = this.makeLatLng(e, index)
            let selectMarkerIndex = this.coordinates.findIndex((marker)=>{
                return marker.index === index;
            });
            this.coordinates[selectMarkerIndex] = Object.assign({}, this.coordinates[selectMarkerIndex], latLng);
            this.currentMarker = Object.assign({}, this.currentMarker, latLng);
            this.makePolylinePush(this.coordinates)
            const coordinates = JSON.parse(JSON.stringify(this.coordinates));
            this.$refs.polyline.value = JSON.stringify(coordinates.map((marker)=>{delete marker.index;return marker})).replace(/\s+/g,'');
        },
        async onChangeText(){
            this.loading = true;
            const deepCopyCoordinates = JSON.parse(JSON.stringify(this.coordinates));
            const isJSON = await this.isValidJson(this.$refs.polyline.value);
            if (isJSON) {
                this.exponentialBackoff = 1000;
                if (this.markers.length!==0) {
                    this.resetMarkersPolyline();
                }
                const polylineValue = JSON.parse(this.$refs.polyline.value);
                //this.$refs.polyline.valueにはindexがない状態で表示されているため、coordinates=valueだとindexが消えてしまいエラーが発生してしまう。なのでObject.assignでマージ
                if(polylineValue.length == this.coordinates.length){
                    this.coordinates = this.coordinates.map((coordinate, i)=>{
                        return Object.assign({}, coordinate, polylineValue[i]);
                    })
                } else { //新たなデータをテキストエリアに入れた時
                    this.coordinates = polylineValue.map((coordinate)=>{　//緯度経度の値はあるが、インデックスがないので新たに作成
                        coordinate = Object.assign({}, coordinate, {index: this.autoIncrement})
                        this.autoIncrement++;
                        return coordinate;
                    })
                }
                this.redraw(this.coordinates); //再描画
                //インスタンスをデータで保持
                this.loading = false;
            } else {
                if (this.$refs.polyline.value=='') {
                    if (this.markers.length!==0) {
                        this.resetMarkersPolyline();
                    }
                    this.loading = false;
                } else {
                    const pow = 2;
                    this.exponentialBackoff = this.exponentialBackoff*pow;
                    const that = this;
                    let timer = setTimeout(function(){that.onChangeText()},that.exponentialBackoff);
                    if(this.exponentialBackoff>=8000){
                        clearInterval(timer);
                        this.exponentialBackoff = 1000;
                        this.coordinates = deepCopyCoordinates;
                        this.loading=false;
                        alert('not json')
                    }
                }
            }
        },
        //makePolylineの返り値を作成し、resetMarkersPolyline関数の後に、マーカーとポリラインをデータに入れる
        redraw(coordinates){
            this.markers = coordinates.map((coordinate)=>{
                return this.makeMarker(coordinate, coordinate.index);
            });
            this.makePolylinePush(coordinates)
        },
        makeLatLng(e, index){
            const lat = (e.latLng).lat();
            const lng = (e.latLng).lng();
            return {"lat": Math.round(lat*1000000)/1000000, "lng": Math.round(lng*1000000)/1000000, index: index};
        },
        makeMarker(latLng, i){ //再描画時はautoIncrementではなく元々ふってあるindexを使うため台に引数にindexを入れる
            const marker = new google.maps.Marker({
                map: this.map,
                position: new google.maps.LatLng(latLng.lat, latLng.lng),
                draggable: true
            });
            let index = JSON.parse(JSON.stringify(i));//deepcopy
            //click marker
            marker.addListener("click", async() => {
                this.resetMarkersPolyline();
                this.coordinates = await this.coordinates.filter((marker)=>{
                    return marker.index !== index;
                });
                this.redraw(this.coordinates);
            });
            //mouseup marker
            marker.addListener("mouseup", (e) => {
                this.onDragMarker(e, index);
            });
            return marker;
        },
        resetAll(){
            if (this.markers.length !==0) {
                this.resetMarkersPolyline();
                this.markers = [];
                this.polyline = null;
                this.coordinates = [];
                this.$refs.polyline.value = null;
            }
        },
        resetMarkersPolyline(){
            this.markers.forEach((marker)=>{
                marker.setMap(null);
            })
            this.polyline.setMap(null);
        },
        makePolylinePush(coordinates){
            const polyline = this.makePolyline(coordinates);
            if (this.polyline) {
                this.polyline.setMap(null);
            }
            this.polyline = polyline;
        },
        makePolyline(coordinates){
            return new google.maps.Polyline( {
                map: this.map ,
                path: coordinates,
                strokeWeight: 3,
            });
        },
        deleteIndexKey(value){
            return JSON.stringify(value.map((marker)=>{delete marker.index;return marker})).replace(/\s+/g,'')
        },
        isValidJson(value) {
            try {
                JSON.parse(value)
                return true;
            } catch (e) {
                return false
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