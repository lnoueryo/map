<template>
    <div>
    <v-container fluid>
        <select v-model="delimiter">
            <option value=",">CSV</option>
            <option value="t">TSV</option>
            <option value="|">|</option>
        </select>
        <v-data-iterator :items="items" :items-per-page.sync="itemsPerPage" :page.sync="page" :search="search" :sort-by="sortBy.toLowerCase()" :sort-desc="sortDesc" hide-default-footer>
        <template v-slot:header>
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
                <v-btn class="ml-2" @click="$refs.input.click()">CSV入力</v-btn>
                <v-btn class="ml-2" @click="getCSV">CSV出力</v-btn>
            </div>
            </v-toolbar>
        </template>

        <template v-slot:default="props">
            <v-row>
            <v-col v-for="(item, i) in props.items" :key="i" cols="12" sm="6" md="4" lg="3">
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
        </template>

        <template v-slot:footer>
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
        </template>
        </v-data-iterator>
    </v-container>
    <v-row justify="center">
    <v-dialog v-model="editDialog" persistent max-width="600px">
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
    </v-row>
    <a ref="download" :href="csv.url" :download="csv.name" style="display:none">CSV</a>
    <input ref="input" type="file" style="display:none" name="" id="" @input="getFiles">
    </div>
</template>

<script lang="ts">

import Vue from 'vue'
import Company from '~/components/management/Company.vue'
import Line from '~/components/management/Line.vue'
import Station from '~/components/management/Station.vue'
interface DataType {
    itemsPerPageArray: number[],
    search: null|string,
    filter: {},
    sortDesc: boolean,
    page: number,
    itemsPerPage: number,
    dataKeys: string[],
    editDialog: boolean,
    componentTypes: string[],
    file: null,
    delimiter: string,
    csv: {url: null|string, name: null|string},
    csvDialog: boolean

}
import { mapGetters } from 'vuex'
export default Vue.extend({
    components:{
    Company,
    'train-line': Line,
    Station
    },
    data(): DataType {
        return {
            itemsPerPageArray: [4, 8, 12, 16, 20, 50, 100],
            search: '',
            filter: {},
            sortDesc: false,
            page: 1,
            itemsPerPage: 4,
            dataKeys: ['company', 'line', 'station'],
            editDialog: false,
            componentTypes: ['company', 'train-line', 'station'],
            file: null,
            delimiter: ',',
            csv: {url: null, name: null},
            csvDialog: false
        }
    },
    computed: {
        ...mapGetters('management', [
            'changeList',
            'sortKeys',
            'items',
        ]),
        numberOfPages () {
            return Math.ceil(this.items.length / (this as any).itemsPerPage)
        },
        filteredKeys () {
            return this.sortKeys.filter((key: string) => key !== 'ID')
        },
        component(){
            return (this as any).componentTypes[this.changeList];
        },
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
        selectedItem:{
            get(){
                return this.$store.getters['management/selectedItem'];
            },
            set(value){
                this.$store.dispatch('management/selectedItem', value)
            }
        }
    },
    watch:{
        data:{
            async handler(){
                this.$store.dispatch('management/items', this.$store.getters['management/data'])
            },
            immediate: true
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
            (this as any).editDialog = true;
            this.$store.dispatch('management/editIndex', index)
        },
        getFiles(e: Event){
            const files = (<HTMLInputElement>e.target).files as FileList;
            (this as any).file = files[0];
            (this as any).csvDialog = true;
        },
        async sendCSV(){
            var formData = new FormData();
            formData.append("file", (this as any).file);
            formData.append("delimiter", (this as any).delimiter);
            this.$axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
            this.$axios.defaults.xsrfCookieName = "csrftoken";
            this.$axios.$post(`/api/management/${(this as any).dataKeys[this.changeList]}/csv/`, formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }
            });
            (this as any).csvDialog = false
        },
        async getCSV(){
            let response = await this.$axios.$get(`/api/management/${(this as any).dataKeys[this.changeList]}/csv/`, {params: {delimiter: (this as any).delimiter}});
            if((this as any).dataKeys[this.changeList]=='line'){response = response.replace(/(""lat"")/g, "\"lat\"").replace(/(""lng"")/g, "\"lng\"").replace(/\"\[/g, "\[").replace(/\]\"/g, "\]")}
            console.log(response)
            const blob = new Blob([ response ], { type: "text/plain" });
            const url =  window.webkitURL.createObjectURL(blob);
            const name = (this as any).dataKeys[this.changeList] + (this as any).timestampToTime() + '.csv';
            this.$set((this as any).csv, 'url', url);
            await this.$set((this as any).csv, 'name', name);
            (this.$refs.download as HTMLAnchorElement).click();
        },
        async saveCompany(){
            try {
                const response = await this.$axios.$post('/api/map/', {name: 'イノウエレイルウェイ', address: '東京都世田谷区松原1-43-14', founded: '1990年9月8日'});
                console.log(response)
            } catch (error) {
                console.log(error.response)
            }
        },
        timestampToTime() {
        const date = new Date();
        const yyyy = `${date.getFullYear()}`;
        const MM = `0${date.getMonth() + 1}`.slice(-2);
        const dd = `0${date.getDate()}`.slice(-2);
        const HH = `0${date.getHours()}`.slice(-2);
        const mm = `0${date.getMinutes()}`.slice(-2);
        const ss = `0${date.getSeconds()}`.slice(-2);

        return `${yyyy}_${MM}${dd}_${HH}${mm}${ss}`;
        }
    },
})
</script>