<template>
    <div>
        <div class="ratio16-9">
            <canvas ref="chart" class="chart"></canvas>
        </div>
        <!-- <v-btn @click="drawTriangle">click</v-btn>
        <v-btn @click="back" :disabled="index==0">back</v-btn>
        <v-btn @click="next">next</v-btn> -->
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
interface dataType {
    chartConfig: ChartConfig,
    horizontalAxis: number[] | string[],
    verticalAxis: number[],
    data: {city: string, population: number[]},
    index: number,
    canvas: Canvas,
    timer: null | NodeJS.Timeout
}
interface ChartConfig {dividedNum: number, heights: number[]}
interface Canvas {chart: HTMLCanvasElement | null, context: CanvasRenderingContext2D | null, width: number, height: number}
interface Context {context: CanvasRenderingContext2D, lineWidth: number, fontSize: number, fillStyle: string, textAlign: CanvasTextAlign, textBaseline: CanvasTextBaseline}
export default Vue.extend({
    data(): dataType {
        return {
            chartConfig: {dividedNum: 13,heights: []},
            horizontalAxis: [1920,1925,1930,1935,1940,1944,1945,1946,1947,1948,1950,1955,1960,1965,1970,1975,1980,1985,1990,1995,2000,2005,2010,2015,2016,2017,2018,2019],//lengthをverticalAxisと揃える
            verticalAxis: [],//lengthをhorizontalAxisと揃える
            data: {city: '', population: []},
            index: 2,
            canvas: {chart: null, context: null, width: 0, height: 0},
            timer: null
        }
    },
    async created() {
        this.data = this.population[this.lineChartIndex];
        this.verticalAxis = this.population[this.lineChartIndex].population
    },
    computed: {
        horizontalAxisFilter() {
            return (this as any).horizontalAxis.filter((_: any, i: number) => {
                return i > 13
            })
        },
        verticalAxisFilter() {
            return (this as any).verticalAxis.filter((_: any, i: number) => {
                return i > 13
            })
        },
        windowSize() {
            return this.$store.getters.windowSize;
        },
        population() {
            return this.$store.getters['station/population'];
        },
        lineChartIndex() {
            return this.$store.getters['station/lineChartIndex'];
        },
    },
    watch: {
        windowSize: {
            handler() {
                !(this as any).time ? this.resetChart() : clearTimeout((this as any).timer)
                const that = this;
                this.timer = setTimeout(() => {
                    that.timer = null
                    that.makeChart()
                }, 200)
            },
            immediate: false
        },
        lineChartIndex() {
            this.resetChart()
            this.makeChart()
        }
    },
    mounted() {
        this.init()
        this.makeChart()
    },
    methods:{
        init() {
            const pixelRatio = 10
            this.canvas.chart = this.$refs.chart as HTMLCanvasElement;
            this.canvas.context = this.canvas.chart.getContext('2d') as CanvasRenderingContext2D;
            this.canvas.chart.width = this.canvas.chart.getBoundingClientRect().width * pixelRatio;
            this.canvas.chart.height = this.canvas.chart.getBoundingClientRect().height * pixelRatio;
            this.canvas.width = this.canvas.chart.getBoundingClientRect().width;
            this.canvas.height = this.canvas.chart.getBoundingClientRect().height;
        },
        makeChart() {
            const pixelRatio = 10
            const canvas = this.canvas;
            const context = canvas.context as CanvasRenderingContext2D;
            const width = canvas.width as number;
            const pixelHeight = pixelRatio * (canvas.height as number)
            const dividedHeight = pixelHeight / this.chartConfig.dividedNum;

            context.save();
            const config: Context = {context: context as CanvasRenderingContext2D, lineWidth: 0.015 * width, fontSize: 0.216 * width, fillStyle: 'orange', textAlign: 'right', textBaseline: 'top'}
            this.setContext(config)

            context.fillText(this.data.city as string, width * 0.92, 0.05 * dividedHeight, 2000);

            this.makeHorizontalAxis(context, width, dividedHeight)
            this.makeVerticalAxis(context, width, dividedHeight)
            this.makeHorizontalAxisText(canvas)
            this.makeVerticalAxisText(canvas)
            this.makeDot(context, width, pixelHeight)
            context.restore();

        },
        setContext(config: Context) {
            config.context.lineWidth = config.lineWidth;
            const fontSize = config.fontSize;
            config.context.font = `${fontSize}px 'ＭＳ ゴシック'`;
            config.context.fillStyle = config.fillStyle;
            config.context.textAlign = config.textAlign;
            config.context.textBaseline = config.textBaseline;
        },
        makeHorizontalAxis(context: CanvasRenderingContext2D, pixelWidth: number, dividedHeight: number) {
            for (let i = this.chartConfig.dividedNum - 1; i > 0; i--) {
                context.strokeStyle = '#cacaca';
                context.lineWidth = 0.015 * pixelWidth;
                context.moveTo(pixelWidth, i * dividedHeight);
                context.lineTo(9 * pixelWidth, i * dividedHeight);
                context.stroke();
                if(i < this.chartConfig.dividedNum && i > 0) this.chartConfig.heights.push(i*dividedHeight);
            }
        },
        makeHorizontalAxisText(canvas: Canvas) {
            const context = canvas.context as CanvasRenderingContext2D;
            const width = canvas.width as number
            const height = canvas.height as number
            const config: Context = {context: context as CanvasRenderingContext2D, lineWidth: 0.015 * width, fontSize: 0.216 * width, fillStyle: 'orange', textAlign: 'center', textBaseline: 'top'}
            this.setContext(config)
            let widths = []
            for (let i = 0; i < this.horizontalAxisFilter.length; i = i + 1 * 8 / this.horizontalAxisFilter.length) {
                widths.push(width + width * i);
            }
            for (let i = 0; i < this.horizontalAxisFilter.length; i++) {
                context.fillText(this.horizontalAxisFilter[i], widths[i], 9.5 * height, 2000);//10はcanvasからはみ出してしまう
            }
            context.restore();
        },
        makeVerticalAxis(context: CanvasRenderingContext2D, pixelWidth: number, dividedHeight: number) {
            context.beginPath();
            context.moveTo(pixelWidth,dividedHeight);
            context.lineTo(pixelWidth,(this.chartConfig.dividedNum-1)*dividedHeight);
            context.closePath();
            context.stroke();
        },
        makeVerticalAxisText(canvas: Canvas) {
            const context = canvas.context as CanvasRenderingContext2D;
            const width = canvas.width as number
            const config: Context = {context: context as CanvasRenderingContext2D, lineWidth: 0.015 * width, fontSize: 0.216 * width, fillStyle: 'orange', textAlign: 'right', textBaseline: 'middle'}
            this.setContext(config)
            const chart = this.chartMaxMin()
            const difference = this.horizontalAxisDiff()
            let values = []
            for (let i = chart.min - difference; i < chart.max+difference+1; i = i + difference) {
                values.push(Math.round(i / 10) * 10)
            }
            for (let i = this.chartConfig.heights.length - 1; i > -1; i--) {
                context.fillText(String(values[i]), width - (width / 10), this.chartConfig.heights[i], 2000);
            }
            context.restore();
        },
        makeDot(context: CanvasRenderingContext2D, width: number, pixelHeight: number) {
            let widths = []
            for (let i = 0; i < this.horizontalAxisFilter.length; i = i + 1 * 8 / this.horizontalAxisFilter.length) {
                widths.push(width + width * i);
            }
            const config: Context = {context: context as CanvasRenderingContext2D, lineWidth: 0.03 * width, fontSize: 0.216 * width, fillStyle: 'orange', textAlign: 'right', textBaseline: 'middle'}
            this.setContext(config)
            context.strokeStyle = 'orange';
            const chart = this.chartMaxMin();
            const difference = this.horizontalAxisDiff();
            const startLine = (this.chartConfig.dividedNum - 2) * pixelHeight / this.chartConfig.dividedNum;
            const heightPerNum = (pixelHeight / this.chartConfig.dividedNum) / difference;
            for (let i = 0; i < widths.length; i++) {
                const diffFromStartLine = this.verticalAxisFilter[i] - chart.min;
                context.beginPath();
                context.arc(widths[i], startLine - (heightPerNum * diffFromStartLine), 40, 0, 2 * Math.PI, true);
                context.fill();
                if(i!==widths.length) {
                    context.moveTo(widths[i], startLine-(heightPerNum * diffFromStartLine));
                    // context.quadraticCurveTo(widths[i+1], height*9-((height*0.75)/dividedNum*(this.verticalAxisFilter[i+1]-minValue)), widths[i], height*9-((height*0.75)/dividedNum*(this.verticalAxisFilter[i]-minValue)));
                    // context.bezierCurveTo(widths[i+1],(height*9-((height*0.75)/dividedNum*(this.verticalAxisFilter[i]-minValue))),widths[i],height*9-((height*0.75)/dividedNum*(this.verticalAxisFilter[i]-minValue)),widths[i+1],height*9-((height*0.75)/dividedNum*(this.verticalAxisFilter[i+1]-minValue)));
                    context.lineTo(widths[i + 1], startLine - (heightPerNum * (this.verticalAxisFilter[i+1] - chart.min)));
                }
                context.stroke();
                context.restore();
            }
        },
        chartMaxMin() {
            const max = this.verticalAxisFilter.reduce((a: number, b: number) => {return Math.max(a, b);});
            const min = this.verticalAxisFilter.reduce((a: number, b: number) => {return Math.min(a, b);});
            const numberOfDigits = String(max - min).length - 3;
            const pow = Math.pow(10, numberOfDigits);
            const maxValue = Math.floor(max / pow) * pow;
            const minValue = Math.floor(min / pow) * pow;
            return {max: maxValue, min: minValue};
        },
        horizontalAxisDiff() {
            const chart = this.chartMaxMin();
            const difference = (chart.max - chart.min) / (this.chartConfig.dividedNum - 4);
            return difference;
        },
        drawTriangle() {
            const chart = this.canvas.chart as HTMLCanvasElement;
            if (chart.getContext) {
                const context = chart.getContext('2d') as CanvasRenderingContext2D;
                // context.strokeStyle = 'rgb(0,0,255)';
                // context.fillStyle = "rgb(0, 0, 255)";
                context.beginPath();
                const width = chart.getBoundingClientRect().width;
                const height = chart.getBoundingClientRect().height;
                context.lineWidth = 0.069 * width;
                context.moveTo(5.17 * width, 1.84 * height);
                context.lineTo(7.76 * width, 9.19 * height);
                context.lineTo(2.59 * width, 9.19 * height);
                context.closePath();
                context.stroke();
            }
        },
        next() {
            this.$store.commit('changeLineChartIndex', 1);
            this.resetChart();
            this.makeChart();
        },
        back() {
            this.$store.commit('changeLineChartIndex', -1);
            this.resetChart();
            this.makeChart();
        },
        resetChart() {
            const canvas = this.canvas;
            const context = canvas.context as CanvasRenderingContext2D;
            const pixelWidth = (canvas.width as number) * 10;
            const pixelHeight = (canvas.height as number) * 10;
            context.clearRect(0, 0, pixelWidth, pixelHeight);
            this.data = {...this.data, ...this.population[this.lineChartIndex]};
            this.verticalAxis = [];
            this.verticalAxis = [...this.verticalAxis, ...this.population[this.lineChartIndex].population]
            this.chartConfig = {...this.chartConfig, ...{heights: []}};
        }
    }
})
</script>

<style lang="scss" scoped>
    .chart {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    .ratio16-9 {
        padding-top: 56.25%;
        width: 100%;
        position: relative;
    }
</style>