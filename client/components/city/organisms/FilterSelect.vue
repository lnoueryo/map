<template>
    <div>
        <div class="top-menu">
            <div class="mb-2">
                <label>市町村</label>
                <item-select maxHeight="calc(100vh - 200px)" style="position:relative;z-index:3" v-model="selectedCityItems" :items="$store.getters['city/cities']" placeholder="市区町村を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
            <div class="mb-2">
                <label>鉄道会社</label>
                <item-select maxHeight="calc(100vh - 300px)" style="position:relative;z-index:2" v-model="selectedCompanyItems" :items="$store.getters['city/companies']" placeholder="鉄道会社名を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
            <div v-if="selectedCompanyItems.length!==0">
                <label>路線</label>
                <item-select maxHeight="calc(100vh - 300px)" style="position:relative;z-index:1" v-model="selectedLineItems" :items="$store.getters['city/lineItems']" placeholder="路線を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
const ItemSelect = () => import('../../global/ItemSelect.vue');
interface Station {name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number};
interface DataType {timer: null | NodeJS.Timer}
interface City {name: string, city_code: string, prefecture_id: string}
export default Vue.extend({
    components:{
        ItemSelect,
    },
    data(): DataType {
        return {
            timer: null
        }
    },
    watch: {
        selectedCompanyItems: {
            handler(newValues, oldValues) {
                if (newValues.length < oldValues.length) {
                    const uncheck = oldValues.filter((oldValue: Station) => {//resetで一気にチェックが外れるので、findを使わない
                        return newValues.filter((newValue: Station) => {return oldValue.id == newValue.id}).length == 0;
                    })
                    this.$store.dispatch('city/uncheck',uncheck)
                }
            }
        }
    },
    computed: {
        selectedCompanyItems: {
            get() {
                return this.$store.getters['city/selectedCompanyItems'];
            },
            set(value) {
                this.clearTime()
                const that = this;
                this.timer = setTimeout(() => {
                that.$store.dispatch('city/selectedCompanyItems', value);
                }, 200)
            }
        },
        selectedLineItems: {
            get() {
                return this.$store.getters['city/selectedLineItems'];
            },
            set(value) {
                this.clearTime()
                const that = this;
                this.timer = setTimeout(() => {
                    that.$store.dispatch('city/selectedLineItems', value);
                }, 250)
            }
        },
        selectedCityItems: {
            get() {
                return this.$store.getters['city/selectedCityItems'];
            },
            set(value: City) {
                this.clearTime()
                const that = this;
                this.timer = setTimeout(() => {
                    that.$store.commit('city/selectedCityItems', value);
                }, 200)
            }
        },
    },
    methods: {
        clearTime() {
            if (this.timer) clearTimeout(this.timer);
        }
    }
})
</script>

<style lang="scss" scoped>
    .top-menu {
        height: 100%;
        max-height: calc(100% - 64px);
    }
</style>