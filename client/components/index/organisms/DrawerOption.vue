<template>
    <div>
        <div class="list-bottom">
            <div class="d-flex my-2 px-3" style="font-size:14px;">
                <toggle-switch class="mr-3" v-model="chartSwitch" id="chartSwitch" background-color="#ff9800" style="width:50%;display:flex;justify-content:space-between">グラフ</toggle-switch>
                <toggle-switch v-model="dotSwitch" id="dotSwitch" background-color="#ff9800" style="width:50%;">ドット</toggle-switch>
            </div>
            <div class="d-flex my-2 px-3" style="font-size:14px;">
                <toggle-switch class="mr-3" v-model="markerSwitch" id="markerSwitch" background-color="#ff9800" style="width:50%;">マーカー</toggle-switch>
                <toggle-switch v-model="lineSwitch" id="lineSwitch" background-color="#ff9800" style="width:50%;">ライン</toggle-switch>
            </div>
            <v-btn color="red" outlined block @click="$parent.onClickCircleButton">閉じる</v-btn>
        </div>
    </div>
</template>

<script>
import Vue from 'vue';
const ToggleSwitch = () => import('../../global/ToggleSwitch.vue');
// import ToggleSwitch from '../../global/ToggleSwitch.vue';
export default Vue.extend({
    components:{
        ToggleSwitch,
    },
    computed:{
        markerSwitch:{
            get(){
                return this.$store.getters['home/markerSwitch'];
            },
            set(value){
                this.$store.dispatch('home/changeMarkerSwitch', value);
            }
        },
        lineSwitch:{
            get(){
                return this.$store.getters['home/lineSwitch'];
            },
            set(value){
                this.$store.dispatch('home/changeLineSwitch', value);
            }
        },
        chartSwitch:{
            get(){
                return this.$store.getters['home/chartSwitch'];
            },
            set(value){
                this.$store.dispatch('home/changeChartSwitch', value);
            }
        },
        dotSwitch:{
            get(){
                return this.$store.getters['home/dotSwitch'];
            },
            set(value){
                this.$store.dispatch('home/changeDotSwitch', value);
            }
        },
    },
    methods:{
        onClickChart(){
            this.$refs.chartInput.click()
        }
    }
})
</script>

<style lang="scss" scoped>
    .list-bottom{
        position:absolute;
        bottom:0;
        right:0;
        left:0;
        z-index:-1;
        margin:auto;
    }
</style>