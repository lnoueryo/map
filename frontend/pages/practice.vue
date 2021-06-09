<template>
    <div>
        <div ref="a" style="padding-top:56.25%;width: 100%;position: relative;">
            <canvas ref="chart" class="chart"></canvas>
        </div>
        <v-btn @click="drawTriangle">click</v-btn>
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
            index: 0,
            chart: null
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
    },
    mounted(){
        this.chart = this.$refs.chart;
        this.chart.width = this.chart.getBoundingClientRect().width
        this.chart.height = this.chart.getBoundingClientRect().height
        console.log(this.chart.getBoundingClientRect())
        // this.chart.width = this.chart.getBoundingClientRect()
    },
    methods:{
        drawTriangle(){
            // const chart = this.chart;
            if (this.chart.getContext) {
                const context = this.chart.getContext('2d');
                context.beginPath();
                //パスの開始座標を指定する
                context.moveTo(100,20);
                //座標を指定してラインを引いていく
                context.lineTo(150,100);
                context.lineTo(50,100);
                //パスを閉じる（最後の座標から開始座標に向けてラインを引く）
                context.closePath();
                //現在のパスを輪郭表示する
                context.stroke();
            }
        }
    }
})
</script>

<style>
    .chart {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color:white;
    }
</style>