<template>
    <div>
        <!-- <div><textarea>{{company}}</textarea></div> -->
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
    data() {
        return {
            map: null,
            overview: null,
            company: []
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