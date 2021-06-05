<template>
    <div>
        <nav :class="drawerClass">
            <div class="display-height">
                <div class="top-menu">
                    <item-select placeholder="鉄道会社名で絞り込む" background-color="white" ripple="true"></item-select>
                </div>
                <div class="list-bottom">
                    <div class="d-flex mb-2 px-2" style="font-size:14px;">
                        <toggle-switch class="mr-4" v-model="markerSwitch" id="markerSwitch" background-color="#ff9800">マーカー</toggle-switch>
                        <toggle-switch v-model="lineSwitch" id="lineSwitch" background-color="#ff9800">ライン</toggle-switch>
                    </div>
                    <v-btn color="red" outlined block @click="onClickCircleButton">閉じる</v-btn>
                </div>
            </div>
        </nav>
        <div id="drawer-button-wrapper">
            <circle-button class="animation" @click.native="onClickCircleButton" :style="drawerClass.open==true?{transform:'translate(-306px,-56px)'}:''"><div class="down-icon rotate"></div></circle-button>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import ToggleSwitch from '../components/ToggleSwitch.vue';
import ItemSelect from '../components/ItemSelect.vue';
import CircleButton from '../components/CircleButton.vue';
interface DataType {drawerClass: {drawer: boolean,open: boolean},markerSwitch:boolean,lineSwitch:boolean}
export default Vue.extend({
    components:{
        ItemSelect,
        CircleButton,
        ToggleSwitch
    },
    data(): DataType {
        return {
            drawerClass: {
                'drawer': true,
                'open': false
            },
            markerSwitch: true,
            lineSwitch: true,
        }
    },
    watch:{
        markerSwitch:{
            handler(v){
                this.$store.dispatch('home/changeMarkerSwitch',v);
            },
            immediate: true
        },
        lineSwitch:{
            handler(v){
                this.$store.dispatch('home/changeLineSwitch',v);
            },
            immediate:true,
        },
    },
    methods:{
        onClickCircleButton(){
            this.drawerClass.open=!this.drawerClass.open;
            this.$parent.$emit('open')
        }
    }
})
</script>

<style lang="scss">
    .display-height{
        position:relative;
        height: 100vh;
        max-height: 100%;
        z-index: -1;
    }
    .drawer{
        padding:5px;
        top: 64px;
        height: 100vh;
        max-height: calc(100% - 64px);
        position: fixed;
        transform: translateX(100%);
        width: 256px;
        right:0;
        background-color: #363636;
        color: #FFFFFF;
        z-index:2;
        transition: all .3s;
        .top-menu{
            height:100%;
            max-height: calc(100% - 64px);
        }
    }
    .open{
        transform: translateX(0%);
        transition: all .3s;
    }
    #drawer-button-wrapper{
        height: 100vh;
        max-height: calc(100% - 64px);
        width:100px;
        position:fixed;
        right:0;
        top:64px;
        z-index:1;
        .animation{
            position: absolute;
            top: 50%;
            left: 50%;
            margin: auto;
            visibility: hidden;
            opacity: 0;
            transform: translateX(100%) translateY(-100%);
            transition: all .5s;
            transition-delay: .3s;
            transition-property: all;
        }
        .down-icon{
            border-radius: 0px 1px 2px 1px;
            border-right:solid 3px #0044a4;
            border-bottom:solid 3px #0044a4;
            height:12px;
            width:12px;
            transform: rotateZ(45deg) translate(-3px,-3px);
            transition: all .5s;
            transition-delay: .3s;
            transition-property: all;
        }
    }
    #drawer-button-wrapper:hover{
        .animation{
            visibility: visible;
            opacity: 1;
            transform: translateX(-50%) translateY(-100%);
            transition: all .5s;
            .down-icon{
                transform: rotateZ(135deg) translate(-3px,-3px);
                transition: all .8s;
            }
        }
    }
    #drawer-button-wrapper:active{
        .animation{
            .rotate {
                animation: r1 3s linear infinite;
                animation-delay: .3s;
            }
        }
    }
    .list-bottom{
        position:absolute;
        bottom:0;
        right:0;
        left:0;
        z-index:-1
    }
    @keyframes r1 {
        0%   { transform: rotate(135deg) translate(-3px,-3px); }
        100% { transform: rotate(495deg) translate(-3px,-3px); }
    }
</style>