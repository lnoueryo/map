<template>
    <div>
        <nav class="bottom-bar">
            <v-btn-toggle v-model="toggle_exclusive" color="indigo" background-color="indigo">
                <v-btn>
                    <v-icon>mdi-train</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-information-outline</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-right</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-justify</v-icon>
                </v-btn>
                <v-btn>
                    <v-icon>mdi-format-align-justify</v-icon>
                </v-btn>
            </v-btn-toggle>
        </nav>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    // data() {
    //     return {
    //         toggle_exclusive: 0
    //     }
    // },
    computed:{
        toggle_exclusive:{
            get(){
                return this.$store.getters['home/selectedList']
            },
            set(newValue){
                this.$store.dispatch('home/changeList',newValue)
            }
        }
    },
    methods:{
        onClickChangeList(){
            this.$store.dispatch('home/changeList')
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