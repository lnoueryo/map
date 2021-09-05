<template>
    <div>
        <div class="main-container">
            <div v-if="twitterInfo.length !== 0">
                <h2 class="text-center">Twitter</h2>
                <div class="py-2" v-for="(twitter, i) in twitterInfo" :key="i">
                    <div class="px-1" style="display:flex;">
                        <div>
                            <img class="avator" :src="twitter.profile_image_url">
                        </div>
                        <div class="px-1">
                            <div>{{twitter.name}}</div>
                            <div>{{changeTime(twitter.created_at)}}</div>
                            <div class="py-1" style="font-size:14px"><span v-html="twitter.text"></span></div>
                        </div>
                    </div>
                    <div v-if="twitter.images.length !== 0">
                        <!-- <div v-for="(image, j) in twitter.images" :key="j">
                        <img style="width:100%" :src="image" alt="">
                        </div> -->
                        <v-carousel hide-delimiters :show-arrows="twitter.images.length !== 1" height="250px">
                            <v-carousel-item
                            v-for="(image,j) in twitter.images"
                            :key="j"
                            :src="image"
                            ></v-carousel-item>
                        </v-carousel>
                    </div>
                </div>
            </div>
            <div v-else class="centering">
                <div>マーカーをクリックしてTwitterの駅情報を取得しましょう</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import {mapGetters} from 'vuex'
export default Vue.extend({
    computed:{
        ...mapGetters('info', [
            'twitterInfo'
        ]),
    },
    methods: {
        changeTime(time: string) {
            let date = new Date(time);
            const  year = date.getFullYear();
            const  month = ("0"+(date.getMonth() + 1)).slice(-2);
            const  day =  ("0"+date.getDate()).slice(-2);
            const  hours =  ("0"+date.getHours()).slice(-2);
            const  minutes =  ("0"+date.getMinutes()).slice(-2);
            const changedDate = `${year}-${month}-${day} ${hours}:${minutes}`
            return changedDate
        }
    }
})
</script>

<style lang="scss" scoped>
    .main-container {
        background-color: white;
        color: black;
        .avator {
            width: 100%;
            border-radius: 50%;
            width: 48px;
            height: 48px;
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
    .centering {
        display: flex;
        align-items: center;
        height: 100%;
    }
</style>