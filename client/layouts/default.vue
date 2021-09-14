<template>
    <v-app dark v-resize="onResize">
        <header-bar></header-bar>
        <nuxt style="padding-top:64px" />
        <!-- <v-main>
            <v-container>
                <nuxt />
            </v-container>
        </v-main> -->
        <!-- <v-footer :absolute="!fixed" app>
        <span>&copy; {{ new Date().getFullYear() }}</span>
        </v-footer> -->
    </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import HeaderBar from '../components/global/HeaderBar.vue'
import {setHeight, invalidHover} from '../utils/smp';

export default Vue.extend({
    components:{
        HeaderBar
    },
    data() {
        return {
            windowSize: {x: 0, y: 0 }
        }
    },
    beforeCreate() {
        if (process.env.NODE_ENV === 'production') {
            if (window.location.hostname === 'map-ai7ganlifq-an.a.run.app') {
                this.$axios.defaults.baseURL = '/'
            }
        }
        this.$store.dispatch('isAuth', this.$route.name)
    },
    mounted () {
        this.onResize();
    },
    methods:{
        onResize () {
            this.$store.dispatch('windowSize', { x: window.innerWidth, y: window.innerHeight })
            setHeight()
            invalidHover();
        },
    }
})
</script>

<style lang="scss">
.labels {
    color: #ffffff;
    background: #000000;
    font-size: 14px;
    text-align: center;
    padding: 2px 10px;
    border-radius: 8px;
}
.gm-style-iw {
  margin-left: 10px;
}
.gm-style-iw > button {
  display: none !important;
}
</style>