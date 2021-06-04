<template>
    <div>
        <nav class="bottom-bar">
            <div>
                <v-btn color="orange" @click="onClickMakePolyline">makepolyline</v-btn>
            </div>
        </nav>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    methods:{
        onClickMakePolyline(){
            this.$parent.$emit('makePolyline')
        }
    }
})
</script>

<style lang="scss">
    .bottom-bar{
        position:fixed;
        bottom:0;
        right:0;
        left:0;
        height:50px;
        background-color: #272727;
        display: flex;
        align-items: center;
    }
</style>