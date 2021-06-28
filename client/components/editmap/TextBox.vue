<template>
    <div>
        <div style="padding:9px">
            <div>
                <div>lat:<input v-model="currentMarker.lat" v-if="currentMarker.lat" @input="editCurrentCoordinate" style="background-color: white" disabled></div>
                <div>lng:<input v-model="currentMarker.lng" v-if="currentMarker.lng" @input="editCurrentCoordinate" style="background-color: white" disabled></div>
            </div>
        </div>
        <v-btn @click="resetAll">リセット</v-btn>
        <v-btn @click="reverse">リバース</v-btn>
        <v-btn @click="save">更新</v-btn>
        <textarea placeholder="JSON形式で記入してください" ref="polyline" cols="30" rows="30" @input="onChangeText" style="width:100%;background-color:white;font-size:12px;word-break:break-all;"></textarea>
    </div>
</template>

<script>
export default {
    props:['map', 'switch'],
    data() {
        return {
            coordinates: [],
            autoIncrement: 0,
            currentMarker: {},
            markers: [],
            polyline: null,
            exponentialBackoff: 1000,
        }
    },
    watch:{
        coordinates(){
            if(this.coordinates){
                this.$refs.polyline.value = this.deleteIndexKey(this.coordinates)
            }
        },
        map(map){
            if(this.switch){
                map.addListener('click', (e)=>{
                    this.onClickMap(e);
                })
                this.markers.forEach((marker)=>{
                    marker.addListener("dragend", (e) => {
                        this.onDragMarker(e, index);
                    });
                    marker.setDraggable(true)
                })
            }
        },
        switch(value){
            this.mapMarkerEvent(value);
        }
    },
    methods:{
        editCurrentCoordinate(){
            this.coordinates = this.coordinates.map((coordinate)=>{
                return coordinate.index == this.currentMarker.index ? Object.assign({}, coordinate, this.currentMarker) : coordinate;
            })
        },
        onClickMap(e){
            const index = this.autoIncrement;
            const latLng = this.makeLatLng(e, index); //クリックしたところの緯度経度及びindexを算出 {lat: '', lng: '', index: ''}
            this.coordinates.push(latLng); //{lat: '', lng: '', index: ''}をデータに格納
            this.makeMarkerPush(latLng, index)
            this.makePolylinePush(this.coordinates)//this.coordinatesはlatLng[] この処理を最後にしないと処理がおかしくなる
            this.currentMarker = Object.assign({}, this.currentMarker, latLng); //現在の緯度経度を表示
            this.autoIncrement++;//次のindexのために+1
        },
        onDragMarker(e, index){
            const latLng = this.makeLatLng(e, index)
            let selectMarkerIndex = this.coordinates.findIndex((marker)=>{ //coordinatesのindexを検索
                return marker.index === index;
            });
            this.coordinates[selectMarkerIndex] = Object.assign({}, this.coordinates[selectMarkerIndex], latLng); //緯度経度を更新
            this.currentMarker = Object.assign({}, this.currentMarker, latLng);
            this.makePolylinePush(this.coordinates); //polylineを再描画
            this.$refs.polyline.value = this.deleteIndexKey(this.coordinates);
        },
        //alertをスナックバーに変更
        async onChangeText(){
            this.$parent.$data.loading = true;
            if (this.$refs.polyline.value=='') {
                this.resetAll();
                this.$parent.$data.loading = false;
            } else {
                const deepCopyCoordinates = JSON.parse(JSON.stringify(this.coordinates));
                const isJSON = await this.isValidJson(this.$refs.polyline.value);
                if (isJSON) {
                    this.setCoordinates();
                    this.$parent.$data.loading = false;
                } else {
                    const pow = 2;
                    this.exponentialBackoff = this.exponentialBackoff*pow;
                    const that = this;
                    let timer = setTimeout(function(){that.onChangeText()},that.exponentialBackoff);
                    if(this.exponentialBackoff>=8000){
                        clearInterval(timer);
                        this.exponentialBackoff = 1000;
                        this.coordinates = deepCopyCoordinates;
                        this.$parent.$data.loading = false;
                        alert('not json');
                    }
                }
            }
        },
        setCoordinates(){
                this.exponentialBackoff = 1000;
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
        },
        reverse(){
            this.coordinates.reverse();
            this.markers.reverse();
        },
        //makePolylineの返り値を作成し、resetMarkersPolyline関数の後に、マーカーとポリラインをデータに入れる
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
            if (this.markers.length!==0) {
                this.polyline.setMap(null);
                this.markers.forEach((marker)=>{
                    marker.setMap(null);
                })
            }
        },
        redraw(coordinates){
            const markers = coordinates.map((coordinate)=>{
                return this.makeMarker(coordinate, coordinate.index);
            });
            const polyline = this.makePolyline(coordinates);
            if(this.markers.length!==0)this.polyline.setMap(null);
            setTimeout(() => {
                if (this.markers.length!==0) {
                    this.markers.forEach((marker)=>{
                        marker.setMap(null);
                    })
                }
                this.markers = markers;
                this.polyline = polyline;
                this.mapMarkerEvent(this.switch);
            }, 100);
        },
        makeLatLng(e, index){
            const lat = (e.latLng).lat();
            const lng = (e.latLng).lng();
            return {"lat": Math.round(lat*1000000)/1000000, "lng": Math.round(lng*1000000)/1000000, index: index};
        },
        makeMarkerPush(latLng, index){
            const marker = this.makeMarker(latLng, index);
            this.markers.push(marker);
        },
        makeMarker(latLng, index){ //再描画時はautoIncrementではなく元々ふってあるindexを使うため台に引数にindexを入れる
            let zIndex = 1;
            if(!this.switch){
                zIndex=0;
            }
            const marker = new google.maps.Marker({
                map: this.map,
                position: new google.maps.LatLng(latLng.lat, latLng.lng),
                draggable: true,
                zIndex: zIndex,
            });
            //click marker
            marker.addListener("click", async() => {
                this.coordinates = await this.coordinates.filter((marker)=>{
                    return marker.index !== index;
                });
                this.redraw(this.coordinates);
            });
            //mouseup marker
            marker.addListener("dragend", (e) => {
                this.onDragMarker(e, index);
            });
            return marker;
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
            const coordinates = JSON.parse(JSON.stringify(value))
            return JSON.stringify(coordinates.map((coordinate)=>{delete coordinate.index;return coordinate})).replace(/\s+/g,'')
        },
        isValidJson(value) {
            try {
                JSON.parse(value)
                return true;
            } catch (e) {
                return false
            }
        },
        mapMarkerEvent(value){
            if(value){
                this.map.addListener('click', (e)=>{
                    this.onClickMap(e);
                })
                this.markers.forEach((marker)=>{
                    marker.setZIndex(1);
                    marker.setDraggable(true);
                })
            } else {
                this.markers.forEach((marker)=>{
                    // google.maps.event.clearListeners(marker, "dragend");
                    marker.setZIndex(0);
                    marker.setDraggable(false);
                })
            }
        }
    }
}
</script>

<style lang="scss">
    textarea::placeholder{
        text-align: center;
        position: absolute;
        top:150px;
        bottom:0;
        left: 0;
        right:0;
        margin:auto
    }
</style>