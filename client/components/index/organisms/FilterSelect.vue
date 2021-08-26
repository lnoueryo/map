<template>
    <div>
        <div class="top-menu">
            <div class="mb-2">
                <label>市町村</label>
                <item-select maxHeight="calc(100vh - 200px)" style="position:relative;z-index:3" v-model="selectedCityItems" :items="$store.getters['home/cities']" placeholder="市区町村を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
            <div class="mb-2">
                <label>鉄道会社</label>
                <item-select maxHeight="calc(100vh - 300px)" style="position:relative;z-index:2" v-model="selectedCompanyItems" :items="$store.getters['home/companies']" placeholder="鉄道会社名を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
            <div v-if="selectedCompanyItems.length!==0">
                <label>路線</label>
                <item-select maxHeight="calc(100vh - 300px)" style="position:relative;z-index:1" v-model="selectedLineItems" :items="$store.getters['home/lineItems']" placeholder="路線を絞り込む" background-color="white" ripple="true"></item-select>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
// import ItemSelect from '../../global/ItemSelect.vue';
const ItemSelect = () => import('../../global/ItemSelect.vue');
interface Company {id: number, name: string, address: string, founded: string, lines: Line[]};
interface Line {id: number, company_id: number, name: string, polygon: Polygon, color: string,stations: Station[]};
interface Station {name: string,id:number,line_id:number,order:number,prefecture:string,lat:number,lng:number,company_id:number};
interface Polygon {lat: number, lng: number}[];
interface DataType {companySettings: Settings, timer: null|NodeJS.Timer}
interface City {name: string,city_code: string,prefecture_id: string}
interface Settings {chipColor: string, maxHeight: string,chipTextColor: string, placeholder: string,backgroundColor:string,ripple:string,items: Company[]}
export default Vue.extend({
    components:{
        ItemSelect,
    },
    data(): DataType {
        return {
            companySettings: {chipColor: '#ff9800',maxHeight: 'calc(100vh - 250px)',chipTextColor: 'black',placeholder: '鉄道会社名を絞り込む',backgroundColor: 'white', ripple: 'true', items: this.$store.getters['home/companies']},
            timer: null
        }
    },
    watch:{
        selectedCompanyItems:{
            handler(newValues, oldValues){
                if (newValues.length < oldValues.length) {
                    const uncheck = oldValues.filter((oldValue: Station)=>{//resetで一気にチェックが外れるので、findを使わない
                        return newValues.filter((newValue: Station)=>{return oldValue.id == newValue.id}).length==0;
                    })
                    this.$store.dispatch('home/uncheck',uncheck)
                }
            }
        }
    },
    computed:{
        selectedCompanyItems: {
            get(){
                return this.$store.getters['home/selectedCompanyItems'];
            },
            set(value){
                this.clearTime()
                const that = this;
                this.timer = setTimeout(function(){
                that.$store.dispatch('home/selectedCompanyItems', value);
                },200)
            }
        },
        selectedLineItems: {
            get(){
                return this.$store.getters['home/selectedLineItems'];
            },
            set(value){
                this.clearTime()
                const that = this;
                this.timer = setTimeout(function(){
                    that.$store.dispatch('home/selectedLineItems', value);
                },250)
            }
        },
        selectedCityItems: {
            get(){
                return this.$store.getters['home/selectedCityItems'];
            },
            set(value: City){
                this.clearTime()
                const that = this;
                this.timer = setTimeout(function(){
                    that.$store.commit('home/selectedCityItems', value);
                },200)
            }
        },
    },
    methods:{
        clearTime(){
            if (this.timer) {
                clearTimeout(this.timer)
            }
        }
    }
})
</script>

<style lang="scss" scoped>
    .top-menu{
        height:100%;
        max-height: calc(100% - 64px);
    }
</style>