<template>
    <div>
        <v-row class="mt-2" align="center" justify="center">
            <div style="position:fixed;bottom:10px;left:10px;">
                <span class="grey--text">Items per page</span>
                <v-menu offset-y>
                    <template v-slot:activator="{ on, attrs }">
                        <v-btn dark text color="primary" class="ml-2" v-bind="attrs" v-on="on">
                        {{ itemsPerPage }}
                        <v-icon>mdi-chevron-down</v-icon>
                        </v-btn>
                    </template>
                    <v-list>
                        <v-list-item v-for="(number, index) in itemsPerPageArray" :key="index" @click="updateItemsPerPage(number)">
                        <v-list-item-title>{{ number }}</v-list-item-title>
                        </v-list-item>
                    </v-list>
                </v-menu>
            </div>

            <v-spacer></v-spacer>

            <div style="position:fixed;bottom:10px;right:10px;">
                <span class="mr-4 grey--text">
                    Page {{ page }} of {{ numberOfPages }}
                </span>
                <v-btn fab dark color="blue darken-3" class="mr-1" @click="formerPage">
                    <v-icon>mdi-chevron-left</v-icon>
                </v-btn>
                <v-btn fab dark color="blue darken-3" class="ml-1" @click="nextPage">
                    <v-icon>mdi-chevron-right</v-icon>
                </v-btn>
            </div>
        </v-row>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
interface DataType {
    page: number,

}
import { mapGetters } from 'vuex'
export default Vue.extend({
    data(): DataType {
        return {
            page: 1,
        }
    },
    computed: {
        ...mapGetters('management', [
            'filterByWord',
            'itemsPerPage',
            'itemsPerPageArray',
        ]),
        numberOfPages () {
            return Math.ceil(this.filterByWord.length / this.$store.getters['management/itemsPerPage'])
        },
        itemsPerPage:{
            get(){
                return this.$store.getters['management/itemsPerPage']
            },
            set(value){
                this.$store.dispatch('management/itemsPerPage', value);
            }
        }
    },
    methods: {
        nextPage () {
            if (this.$data.page + 1 <= (this as any).numberOfPages) this.$data.page += 1
        },
        formerPage () {
            if (this.$data.page - 1 >= 1) this.$data.page -= 1
        },
        updateItemsPerPage (number: number) {
            this.itemsPerPage = number
        },
    }
})
</script>
