<template>
    <div>
        <a :href="csv" download="hello.csv">CSV</a>
        <div><textarea>{{company}}</textarea></div>
        <input type="file" name="" id="" @input="getFiles">
        <v-btn color="orange" @click="sendCSV">import</v-btn>
        <v-btn color="orange" @click="getCSV">export</v-btn>
        <v-btn color="orange" @click="saveCompany">登録</v-btn>
        <select v-model="table">
            <option value="0">Company</option>
            <option value="1">Line</option>
            <option value="2">Station</option>
        </select>
        <select v-model="delimiter">
            <option value=",">CSV</option>
            <option value="t">TSV</option>
            <option value="|">|</option>
        </select>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
    data() {
        return {
            map: null,
            overview: null,
            company: [],
            csvData: null,
            files: null,
            table: 0,
            delimiter: ',',
            csv: null
        }
    },
    async mounted(){
        const response = await this.$axios.$get('/api/map/');
        this.company = response;
    },
    methods:{
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
        getFiles(e){
            // console.log(e.target.files[0]
            this.files = e.target.files[0];
            // const file = e.target.files[0];
            // const reader = new FileReader();
            // reader.onload=(e)=>{
            //     this.csvData = e.target.result;
            // }
            // reader.readAsDataURL(file);
        },
        async sendCSV(){
            // const response = this.$axios.$post('/api/map/csv/', {csv: this.csvData});
            var formData = new FormData();
            console.log(this.files)
            formData.append("file", this.files);
            this.$axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            this.$axios.defaults.xsrfCookieName = "csrftoken";
            this.$axios.$post('/api/map/csv/', formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }
            })
        },
        async getCSV(){
            const response = await this.$axios.$get('/api/map/csv/', {params: {table: this.table, delimiter: this.delimiter}});
            var txt = "任意のテキスト";
            var blob = new Blob([ response ], { type: "text/plain" });
            this.csv = window.webkitURL.createObjectURL(blob);
        },
        async saveCompany(){
            try {
                const response = await this.$axios.$post('/api/map/', {name: 'イノウエレイルウェイ', address: '東京都世田谷区松原1-43-14', founded: '1990年9月8日'});
                console.log(response)
            } catch (error) {
                console.log(error.response)
            }
        }
    }
})
</script>

<style lang="scss" scoped>
    #map {
        height: 100%;
        position: relative;
        padding-top: 56.25%;
    }
    #overview-wrapper{
        position:absolute;
        width: 30%;
        bottom: 50px;
        left: 15px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.7);
        #overview-container {
            position: relative;
            width: 100%;
            #overview {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
            }
        }
        #overview-container:before {
            content:"";
            display: block;
            padding-top: 56.25%;
        }
    }
</style>