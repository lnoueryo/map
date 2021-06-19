<template>
    <div>
        <div class="d-flex">
            <v-row>
                <v-col v-for="(item, i) in filterByWord" :key="i" cols="12" sm="6" md="4" lg="3">
                    <v-card>
                    <v-card-title class="subheading font-weight-bold d-flex" style="justify-content:space-between">
                        <div>{{ item.name }}</div>
                        <div><v-btn color="orange" @click="edit(i)">編集</v-btn></div>
                    </v-card-title>

                    <v-divider></v-divider>

                    <v-list dense>
                        <v-list-item v-for="(key, j) in filteredKeys" :key="j">
                        <v-list-item-content :class="{ 'blue--text': sortBy === key }">
                            {{ key }}:
                        </v-list-item-content>
                        <v-list-item-content class="align-end" :class="{ 'blue--text': sortBy === key }">
                            {{omittedContent(item[key.toLowerCase()])}}
                        </v-list-item-content>
                        </v-list-item>
                    </v-list>
                    </v-card>
                </v-col>
            </v-row>
            <div>
                <div  class="animation" :class="{'animation-open' : open}" ref="drawer"></div>
                <div class="drawer" :class="{'drawer-open' : open}">
                    <!-- <select v-model="delimiter">
                        <option value=",">CSV</option>
                        <option value="t">TSV</option>
                        <option value="|">|</option>
                    </select>
                    <v-btn class="ml-2" @click="$refs.input.click()">CSV入力</v-btn>
                    <v-btn class="ml-2" @click="getCSV">CSV出力</v-btn> -->
                </div>
            </div>
        </div>
    <!-- <v-dialog v-model="editDialog" persistent max-width="600px">
        <v-card>
        <v-card-title>
            <span class="text-h5">{{data}}</span>
        </v-card-title>
        <v-card-text>
            <v-container>
                <div v-model="selectedItem" :is="component"></div>
            </v-container>
            <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="editDialog = false">
            Close
            </v-btn>
            <v-btn color="blue darken-1" text @click="editDialog = false">
            Save
            </v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
    <v-dialog v-model="csvDialog" persistent max-width="600px">
        <v-card>
        <v-card-title>
            <span class="text-h5">CSVをインポート</span>
        </v-card-title>
        <v-card-text>
            <v-container>
                インポートしますか？
            <select v-model="delimiter">
                <option value=",">CSV</option>
                <option value="t">TSV</option>
                <option value="|">|</option>
            </select>
            </v-container>
            <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="csvDialog = false">
            Close
            </v-btn>
            <v-btn color="blue darken-1" text @click="sendCSV">
            Save
            </v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
    <a ref="download" :href="csv.url" :download="csv.name" style="display:none">CSV</a>
    <input ref="input" type="file" style="display:none" name="" id="" @input="getFiles"> -->
    </div>
</template>

<script lang="ts">

import Vue from 'vue'
import TopBar from '~/components/management/templates/TopBar.vue'
interface DataType {
    filter: {},
    page: number,
    open: boolean

}
import { mapGetters } from 'vuex'
export default Vue.extend({
    components:{
    TopBar
    },
    data(): DataType {
        return {
            open: false,
            filter: {},
            page: 1,
        }
    },
    computed: {
        ...mapGetters('management', [
            'changeList',
            'sortKeys',
            'sortBy',
            'filterByKey',
            'filterByWord',
            'itemsPerPage',
            'itemsPerPageArray',
        ]),
        numberOfPages () {
            return Math.ceil(this.filterByWord.length / (this as any).itemsPerPage)
        },
        filteredKeys () {
            return this.sortKeys.filter((key: string) => key !== 'ID')
        },
        component(){
            return (this as any).componentTypes[this.changeList];
        },
        selectedItem:{
            get(){
                return this.$store.getters['management/selectedItem'];
            },
            set(value){
                this.$store.dispatch('management/selectedItem', value)
            }
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
            if ((this as any).page + 1 <= (this as any).numberOfPages) (this as any).page += 1
        },
        formerPage () {
            if ((this as any).page - 1 >= 1) (this as any).page -= 1
        },
        updateItemsPerPage (number: number) {
            (this as any).itemsPerPage = number
        },
        omittedContent(string: string) {
            const MAX_LENGTH = 50;
            if (Array.isArray(string)) {
                string = JSON.stringify(string)
            }
            if (string && string.length > MAX_LENGTH) {
                return string.substr(0, MAX_LENGTH) + '...';
            }
            return string;
        },
        edit(index: number){
            this.$store.dispatch('management/editIndex', index)
        },
    },
})
</script>

<style lang="scss">
    .animation{
        width:0;
        transform: translateX(50px);
        transition: all .3s;
    }
    .animation-open{
        width:280px;
    }
    .drawer{
        width:280px;
        right: -280px;
        position: fixed;
        transition: all .3s;
        padding: 15px;
    }
    .drawer-open{
        right: 12px;
    }
</style>