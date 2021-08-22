<template>
    <div>
        <div style="height:100vh;background-color:white;color:black;overflow-x:hidden;overflow-y:scroll;max-height:calc(100vh - 238px);">
            <div v-html="cityWikiInfo" v-if="cityWikiInfo"></div>
            <div v-else style="display:flex;align-items:center;height:100%;">
                <div>地図をクリックして町情報を取得しましょう</div>
            </div>
        </div>
        <div class="url-box">
            <a :href="URL" target="_blank">{{URL}}</a>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import {mapGetters} from 'vuex'
export default Vue.extend({
    computed:{
        ...mapGetters('home', [
            'lines',
            'markerSwitch',
            'lineSwitch',
            'selectedMarker',
            'showNumberOfMarkers',
            'searchStations',
            'stationInfo',
            'cityWikiInfo',
        ]),
        URL(){
            if (this.selectedMarker.station_name) {
                return 'https://ja.wikipedia.org/wiki/' + this.selectedMarker.name + '駅'
            }else {
                return;
            }
        }
    },
})
</script>

<style lang="scss" scoped>
    .url-box{
        text-align:center;
        position:relative;
        bottom:0;
        font-size:14px;
        word-break:break-all;
        font-weight:bold;
        background-color:white;
        padding-right:5px;
        padding-top:3px;
    }
</style>