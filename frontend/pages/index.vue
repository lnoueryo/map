<template>
    <div id="wrapper">
        <div>
            <right-drawer></right-drawer>
        </div>
        <div id="container" :class="{'open': open}">
            <div class="main-view">
                <div>
                    <left-list></left-list>
                </div>
                <div class="map-container">
                    <map-view></map-view>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import RightDrawer from '../components/index/templates/RightDrawer.vue'
import LeftList from '../components/index/templates/LeftList.vue'
import MapView from '../components/index/templates/Map.vue'
interface DataType {open: boolean}
export default Vue.extend({
    components: {
        RightDrawer,
        LeftList,
        MapView
    },
    data(): DataType {
        return {
            open: false,
        }
    },
    beforeCreate(){
        this.$store.dispatch('home/getCompanies');
    },
    mounted(){
        this.$on('open', this.drawer);
    },
    methods:{
        drawer(){ //right-drawerが開いた時の処理
            this.open=!this.open;
        },
    }
})
</script>

<style lang="scss" scoped>
    #wrapper{
        max-height:calc(100vh);
        overflow:hidden;
        #container {
            height: 100%;
            width: 100%;
            position:relative;
            padding-right:100px;
            transition: all .3s;
            .main-view{
                display:flex;
                overflow:hidden;
                max-height:calc(100%-200px);
                .map-container{
                    position:relative;
                    width:100%;
                }
            }
        }
        #container.open{
            padding-right: 256px;
            transition: all .3s;
        }
    }
</style>