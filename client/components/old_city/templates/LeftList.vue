<template>
    <div>
        <div class="left-list" :style="{width: width+'px'}">
            <v-btn-toggle mandatory v-model="changeList" color="indigo" background-color="#2f2f2f">
                <v-btn v-for="(button,i) in buttons" :key="i">
                    <v-icon>mdi-{{button}}</v-icon>
                </v-btn>
            </v-btn-toggle>
            <div class="list-top">
                <search-items ref="searchItem"></search-items>
            </div>
            <keep-alive>
                <transition name="fade">
                    <div :is="component"></div>
                </transition>
            </keep-alive>
        <div class="resize" @mousedown="dragStart"></div>
        </div>
    </div>
</template>

<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_name: string, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_name: string, id: number, line_name: string, order: number, pref_name: string, lat: number, lng: number, name: string}
interface DataType {width: number, buttons: string[]};
interface DomEvent extends Event {clientX: number,clientY: number}
import Vue from 'vue';
const MarkerLists = () => import('../organisms/MarkerLists.vue');
const CityWiki = () => import('../organisms/CityWiki.vue');
const StationWiki = () => import('../organisms/StationWiki.vue');
const SearchItems = () => import('../organisms/SearchItems.vue');
const Event = () => import('../organisms/Event.vue');
const Twitter = () => import('../organisms/Twitter.vue');
const SearchBar = () => import('../../global/SearchBar.vue');


export default Vue.extend({
    components: {
        MarkerLists,
        StationWiki,
        SearchBar,
        SearchItems,
        Event,
        CityWiki,
        Twitter,
    },
    data(): DataType {
        return {
            width: 315,
            buttons: ['train', 'information-outline', 'format-align-right', 'city', 'twitter']
        }
    },
    computed: {
        component() {
            const componentTypes = ['marker-lists', 'station-wiki', 'event', 'city-wiki', 'twitter'];
            return componentTypes[(this as any).$store.getters['switch/changeList']];
        },
        changeList: {
            get() {
                return (this as any).$store.getters['switch/changeList'];
            },
            set(newValue) {
                (this as any).$store.dispatch('switch/changeList', newValue);
            }
        },
    },
    methods: {
        limit(e: DomEvent) {
            if (e.clientX < 500 && e.clientX > 100) {
                this.$data.width = e.clientX
            }
        },
        dragStart() {
            const that = this;
            const limit = (e: DomEvent) => {(that as any).limit(e)};
            (this as any).$root.$el.addEventListener('mousemove', limit);
            (this as any).$root.$el.addEventListener('mouseup', () => {(that as any).$root.$el.removeEventListener('mousemove',limit), {once:true}});
        },
    }
})
</script>

<style lang="scss" scoped>
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
        transition: opacity .5s;
    }
    .resize{
        position:absolute;
        top:0;
        bottom:0;
        right:-3px;
        width:6px;
        z-index:5;
        cursor:ew-resize;
    }
    .left-list{
        height:100vh;
        width:100%;
        background-color: #363636;
        position:relative;
        max-height: calc(var(--vh, 1vh) * 100 - 114px);
        margin-bottom:100px
    }
    .list-top{
        padding:10px;
        padding-right:5px;
        text-align:center;
        border-radius:5px;
        color:#363636;
        background-color:white;
        position:relative;
        width:100%;
    }
</style>