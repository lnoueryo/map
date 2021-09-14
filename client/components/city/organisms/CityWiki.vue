<template>
  <div>
    <div class="main-container">
        <div v-html="cityWikiInfo" v-if="cityWikiInfo"></div>
        <div v-else class="centering">
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
        ...mapGetters('city', [
            'selectedMarker',
        ]),
        ...mapGetters('info', [
            'cityWikiInfo',
        ]),
        URL() {
            const url = 'https://ja.wikipedia.org/wiki/' + this.selectedMarker.name;
            return this.selectedMarker.name ? url : null;
        }
    },
})
</script>

<style lang="scss" scoped>
.main-container {
    height: 100vh;
    // max-height: calc(100vh - 238px);
    max-height: calc(var(--vh, 1vh) * 100 - 238px);
    background-color: white;
    color: black;
    overflow-x: hidden;
    overflow-y: scroll;
    .centering {
        display: flex;
        align-items: center;
        height: 100%;
    }
}
.url-box {
    text-align: center;
    position: relative;
    bottom: 0;
    font-size: 14px;
    word-break: break-all;
    font-weight: bold;
    background-color: white;
    padding-right: 5px;
    padding-top: 3px;
}
</style>