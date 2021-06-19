<template>
    <div>
        <v-toolbar dark color="blue darken-3" class="mb-1">
            <v-select v-model="data" flat solo-inverted hide-details :items="dataKeys" prepend-inner-icon="mdi-magnify" label="data"></v-select>
            <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-spacer></v-spacer>
                <v-text-field v-model="search" clearable flat solo-inverted hide-details prepend-inner-icon="mdi-magnify" label="Search"></v-text-field>
                <v-spacer></v-spacer>
                <v-select v-model="sortBy" flat solo-inverted hide-details :items="sortKeys" prepend-inner-icon="mdi-magnify" label="Sort by"></v-select>
                <v-spacer></v-spacer>
                <v-btn-toggle v-model="sortDesc" mandatory>
                    <v-btn large depressed color="blue" :value="false">
                        <v-icon>mdi-arrow-up</v-icon>
                    </v-btn>
                    <v-btn large depressed color="blue" :value="true">
                        <v-icon>mdi-arrow-down</v-icon>
                    </v-btn>
                </v-btn-toggle>
            </template>
            <div class="d-flex">
                <v-btn class="ml-4" @click="$parent.open=!$parent.open">open</v-btn>
            </div>
        </v-toolbar>
    </div>
</template>

<script lang="ts">

import Vue from 'vue'

import { mapGetters } from 'vuex'
export default Vue.extend({
    data(){
        return{
            dataKeys: ['company', 'line', 'station'],
        }
    },
    computed: {
        data:{
            get(){
                return this.$store.getters['management/data'];
            },
            set(value){
                this.$store.dispatch('management/data', value);
            }
        },
        sortBy:{
            get(){
                return this.$store.getters['management/sortBy'];
            },
            set(value){
                this.$store.dispatch('management/sortBy', value);
            }
        },
        sortDesc:{
            get(){
                return this.$store.getters['management/sortDesc'];
            },
            set(value){
                this.$store.dispatch('management/sortDesc', value);
            }
        },
        search:{
            get(){
                return this.$store.getters['management/search'];
            },
            set(value){
                this.$store.dispatch('management/search', value);
            }
        },
        sortKeys(){
            return this.$store.getters['management/sortKeys']
        },
    },
    watch:{
        data:{
            async handler(){
                this.$store.dispatch('management/items', this.$store.getters['management/data'])
            },
            immediate: true
        }
    },
})
</script>
