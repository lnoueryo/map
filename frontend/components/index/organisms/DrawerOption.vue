<template>
    <div>
        <div class="list-bottom">
            <div class="d-flex mb-2 px-2" style="font-size:14px;">
                <toggle-switch class="mr-4" v-model="markerSwitch" id="markerSwitch" background-color="#ff9800">マーカー</toggle-switch>
                <toggle-switch v-model="lineSwitch" id="lineSwitch" background-color="#ff9800">ライン</toggle-switch>
            </div>
            <v-btn color="red" outlined block @click="$parent.onClickCircleButton">閉じる</v-btn>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ToggleSwitch from '../../global/ToggleSwitch.vue';
export default Vue.extend({
    components:{
        ToggleSwitch,
    },
    computed:{
        markerSwitch:{
            get(){
                return this.$store.getters['home/markerSwitch']
            },
            set(value){
                this.$store.dispatch('home/changeMarkerSwitch', value);
            }
        },
        lineSwitch:{
            get(){
                return this.$store.getters['home/lineSwitch']
            },
            set(value){
                this.$store.dispatch('home/changeLineSwitch', value);
            }
        },
    },
})
</script>

<style lang="scss" scoped>
    .list-bottom{
        position:absolute;
        bottom:0;
        right:0;
        left:0;
        z-index:-1
    }
</style>