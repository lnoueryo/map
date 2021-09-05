<template>
    <div>
        <transition name="fade">
            <div class="middle-list">
                <simple-lists :items="prefectures" @item="prefecture={...prefecture, ...$event}" v-if="!$route.query.prefecture_id">都道府県を選択してください</simple-lists>
                <simple-lists :items="selectedPrefecture.cities" @item="city={...city, ...$event}" v-if="$route.query.prefecture_id && !$route.query.city_code">
                    <div @click="getWiki(selectedPrefecture)">{{selectedPrefecture.name}}</div>
                </simple-lists>
                <simple-lists :items="selectedCity.spots" @item="spot={...spot, ...$event}" v-if="$route.query.prefecture_id && $route.query.city_code">
                    <div @click="getWiki(selectedCity)">{{selectedCity.name}}</div>
                </simple-lists>
            </div>
        </transition>
        <half-modal ref=wiki :show="wikiReady" @hide="hideWiki" difference="164px">
            <wiki-info :wiki-data="cityWikiInfo"></wiki-info>
        </half-modal>
        <half-modal ref="places" :show="placesReady" @hide="hidePlaces" difference="164px">
            <div>
                <places-info :places-data="spotDetail"></places-info>
            </div>
            <div>
                <twitter></twitter>
            </div>
        </half-modal>
    </div>
</template>


<script lang="ts">
interface Prefecture {id: string, name: string, wiki: string, lat: number, lng: number, cities: City[]}
interface City   {name: string, wiki: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: Spot[]}
interface Spot {id: number, name: string, place_id: string, address: string, lat: number, lng: number, prefecture_id: string, city_code: string, geohash: string}
interface DataType {listNum: number, prefecture: Prefecture | null, city: City | null, spot: Spot | null, wikiReady: boolean, placesReady: boolean, currentWikiData: string}
import Vue from 'vue';
const SimpleLists = () => import('../../global/SimpleLists.vue');
const HalfModal = () => import('../../global/HalfModal.vue');
const WikiInfo = () => import('../../global/WikiInfo.vue');
const PlacesInfo = () => import('../../global/PlacesInfo.vue');
const Twitter = () => import('../organisms/Twitter.vue');
import { mapGetters } from 'vuex';
export default Vue.extend({
    components: {
        SimpleLists,
        HalfModal,
        WikiInfo,
        PlacesInfo,
        Twitter
    },
    data(): DataType {
        return {
            listNum: 0,
            prefecture: null,
            city: null,
            spot: null,
            wikiReady: false,
            placesReady: false,
            currentWikiData: '',
        }
    },
    computed: {
        ...mapGetters('home', [
            'selectedPrefectureItems',
            'selectedCityItems',
            'prefectures',
            'cities',
            'spots',
        ]),
        ...mapGetters('switch', [
            'markerSwitch',
            'markerSwitches'
        ]),
        ...mapGetters('info', [
            'cityWikiInfo',
            'spotDetail',
        ]),
        selectPrefecture: {
            get() {
                console.log(this.selectedPrefectureItems)
                return this.selectedPrefectureItems;
            },
            set(value) {
                this.$store.dispatch('home/selectedPrefectureItems', value)
            }
        },
        selectCity: {
            get() {
                return this.$store.getters['home/selectedCityItems']
            },
            set(value) {
                this.$store.dispatch('home/selectedCityItems', value)
            }
        },
        selectedPrefecture() {
            // const prefecture = this.prefectures.find((prefecture) => prefecture.id == this.$route.query.prefecture_id)
            return this.prefectures.find((prefecture: Prefecture) => prefecture.id == this.$route.query.prefecture_id);
        },
        selectedCity() {
            return this.cities.find((city: City) => city.city_code == this.$route.query.city_code);
        }
    },
    watch: {
        prefecture(v) {
            const query = {...this.$route.query, ...{prefecture_id: v.id}}
            this.$router.push({query: query})
        },
        city(v) {
            const query = {...this.$route.query, ...{city_code: v.city_code}}
            this.$router.push({query: query})
        },
        spot(v) {
            if((this as any).currentPlacesData == v.name) {
                (this as any).placesReady = true;
            } else {
                (this as any).currentPlacesData = v.name
                this.$store.dispatch('info/spotDetail', v)
                this.$store.dispatch('info/getTwitterInfo', v)
                const wiki = this.$refs.wiki as any;
                wiki.fade()
            }
        },
        cityWikiInfo(v) {
            if(v) {
                (this as any).wikiReady = true;
            }
        },
        spotDetail(v) {
            if(v) {
                (this as any).placesReady = true;
            }
        }
    },
    methods:{
        // checkQuery() {
        //     const query = this.$route.query;
        //     query.prefecture_id && query.city_code
        //                         ? this.listNum = 2 : query.prefecture_id
        //                         ? this.listNum = 1
        //                         : this.listNum = 0;
        // },
        back() {
            const query = {...{}, ...this.$route.query} as any
            const queryArray = Object.keys(this.$route.query)
            if(queryArray.length !== 0) delete query[queryArray.slice(-1)[0]]
            delete query[queryArray.slice(-1)[0]]
            this.$router.push({query: query})
        },
        getWiki(obj: City | Prefecture) {
            if((this as any).currentWikiData == obj.name) {
                (this as any).wikiReady = true;
            } else {
                (this as any).currentWikiData = obj.name
                this.$store.dispatch('info/getCityWikiInfo', {name: obj.wiki});
                const places = this.$refs.places as any;
                places.fade()
            }
        },
        hideWiki() {
            (this as any).wikiReady = false;
        },
        hidePlaces() {
            (this as any).placesReady = false;
        }
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
        max-height: calc(100vh - 165px);
        // max-height: calc(100vh - 212px);
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