<template>
    <div>
        <canvas ref="chart"></canvas>
        <div class="d-flex" v-for="(value, i) in verticalAxisFilter" :key="i">
            <div>{{value}}</div>
            <div v-for="(value, i) in horizontalAxisFilter" :key="i">a</div>
        </div>
        <div class="d-flex">
            <div>{{data.city}}</div>
            <div v-for="(value, i) in horizontalAxisFilter" :key="i">
                {{value}}
            </div>
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import populationData from '~/assets/json/population.json'
export default Vue.extend({
    data() {
        return {
            horizontalAxis: [1920,1925,1930,1935,1940,1944,1945,1946,1947,1948,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2016,2017,2018,2019],
            verticalAxis: [],
            data: {},
            index: 0
        }
    },
    created(){
        this.data = populationData[this.index];
        this.verticalAxis = populationData[this.index].population
    },
    computed: {
        horizontalAxisFilter(){
            return this.horizontalAxis.filter((_, i)=>{
                return i>13
            })
        },
        verticalAxisFilter(){
            return this.verticalAxis.filter((_, i)=>{
                return i>13
            })
        },
    }
})
</script>