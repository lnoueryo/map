<template>
    <div>
        <div v-for="(lists, j) in listTitle" :key="j" style="position:relative;">
            <transition name="list">
                <div v-if="$mapConfig.boundsFilter(lists[field]).length !== 0">
                    <label class="line-name" :style="{backgroundColor: lists.color}" :for="lists.name">
                        <input :id="lists.name" type="checkbox" :value="lists" v-model="firstInputValue" style="display:none;">{{lists.name}}
                    </label>
                    <!-- <label class="line-name" :style="{backgroundColor: line.color}" :for="line.name"><input :id="line.name" type="checkbox" :value="line" v-model="selectLine" style="display:none;">{{line.name}}</label> -->
                </div>
            </transition>
            <transition-group name="list" tag="div">
                <div class="station-list" style="width:100%;color:black" v-for="(list, k) in $mapConfig.boundsFilter(lists[field])" :key="k" @click="onClickList(list)" @mouseover="showInfoWindow(list)" @mouseout="hideInfoWindow">
                    <div>{{list.name}}</div>
                </div>
            </transition-group>
        </div>
    </div>
</template>


<script lang="ts">
interface LinePolyline {lat: number, lng: number}
interface Line {id: number, company_id: number, name: string, polygon: LinePolyline[], color: string, stations: Station[]}
interface Station {company_id: number, id: number, line_id: number, order: number, pref_name: string, lat: number, lng: number, name: string}

import Vue from 'vue';
import { mapGetters } from 'vuex';
export default Vue.extend({
    props: ['listTitle', 'field', 'firstInput', 'secondInput'],
    computed: {
        ...mapGetters('home', [
            'lines',
            'filteredLines',
            'selectedMarker',
            'companies',
            'selectedCompanyItems',
            'selectedLineItems',
            'cities',
        ]),
        ...mapGetters('switch', [
            'markerSwitch',
            'markerSwitches'
        ]),
        firstInputValue: {
            get() {
                return this.firstInput;
            },
            set(newValue) {
                this.$emit("firstInput", newValue);
            },
        },
        secondInputValue: {
            get() {
                return this.secondInput;
            },
            set(newValue) {
                this.$emit("secondInput", newValue);
            },
        },
    },
    methods:{
        onClickList(list: Station) {
            this.$emit('secondInput', list)
        },
        showInfoWindow(spot: any) {
            this.$mapConfig.createMapInfoWindow(spot.lat, spot.lng, spot.name)
        },
        hideInfoWindow(spot: any) {
            this.$mapConfig.infoWindow.setMap(null)
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
    }
    .middle-list {
        overflow-y: scroll;
        overflow-x: hidden;
        height: 100vh;
        max-height: calc(100vh - 213px);
        transition: all .5s;
        .company-name {
            text-align: center;
            border-radius: 5px;
            color: white;
            background-color: #363636;
            width: 100%;
            display: block;
            padding: 10px;
            transition: all .5s;
            cursor: pointer;
        }
        .company-name:hover {
            opacity: .7;
            transition: all .5s;
        }
        .company-name:active {
            opacity: .9;
            transition: all .5s;
        }
        .line-name {
            text-align: center;
            border-radius: 5px;
            color: white;
            width: 100%;
            display: block;
            padding: 10px;
            transition: all .5s;
            cursor: pointer;
        }
        .line-name:hover {
            opacity: .7;
            transition: all .5s
        }
        .line-name:active {
            opacity: .9;
        }
        .list-move {
            transition: transform 1s;
        }
        .list-enter {
            opacity: 0;
            transform: translateX(256px);
        }
        .list-enter-active {
            transition: all 1s;
        }
        .list-leave-active {
            transition: all 1s;
            position: absolute;
        }
        .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
            opacity: 0;
            transform: translateX(256px);
        }
    }
    .station-list {
        padding: 10px;
        background-color: white;
        width: 100%;
        transition: all .5s;
        cursor: pointer;
    }
    .station-list:hover {
        opacity: 0.7;
        transition: all .5s;
    }
    .station-list:active {
        opacity: 0.9;
        transition: all .5s;
    }
</style>