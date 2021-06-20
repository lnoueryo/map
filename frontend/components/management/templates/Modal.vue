<template>
    <div>
        <v-dialog v-model="editDialog" persistent max-width="600px">
            <v-card>
            <v-card-title>
                <span class="text-h5">{{$store.data}}</span>
            </v-card-title>
            <v-card-text>
                <!-- <v-container> -->
                <v-container v-if="selectedItem">
                    <div v-model="selectedItem" :is="component"></div>
                </v-container>
                <small>*indicates required field</small>
            </v-card-text>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="$store.dispatch('management/editIndex',-1)">
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
        <input ref="input" type="file" style="display:none" name="" id="" @input="getFiles">
    </div>
</template>

<script lang="ts">

import Vue from 'vue'
import Company from '~/components/management/organisms/Company.vue'
import Line from '~/components/management/organisms/Line.vue'
import Station from '~/components/management/organisms/Station.vue'
import TopBar from '~/components/management/templates/TopBar.vue'
interface DataType {
    page: number,
    file: null,
    delimiter: string,
    csv: {url: null|string, name: null|string},
    csvDialog: boolean,

}
export default Vue.extend({
    components:{
    Company,
    'train-line': Line,
    Station,
    TopBar

    },
    data(): DataType {
        return {
            page: 1,
            file: null,
            delimiter: ',',
            csv: {url: null, name: null},
            csvDialog: false
        }
    },
    computed: {
        selectedItem(){
            return this.$store.getters['management/selectedItem']
        },
        changeList(){
            return this.$store.getters['management/changeList'];
        },
        editIndex(){
            return this.$store.getters['management/editIndex']
        },
        editDialog(){
            return this.$store.getters['management/editDialog'];
        },
        component(){
            return this.$store.getters['management/component'];
        },
    },
    methods: {
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
            this.$axios.$post(`/api/management/${(this as any).dataKeys[this.$data.changeList]}/csv/`, formData, {
                headers: {
                'Content-Type': 'multipart/form-data'
                }
            });
            (this as any).csvDialog = false
        },
        async getCSV(){
            const changeList = this.$data.changeList;
            let response = await this.$axios.$get(`/api/management/${(this as any).dataKeys[changeList]}/csv/`, {params: {delimiter: (this as any).delimiter}});
            if((this as any).dataKeys[changeList]=='line'){response = response.replace(/(""lat"")/g, "\"lat\"").replace(/(""lng"")/g, "\"lng\"").replace(/\"\[/g, "\[").replace(/\]\"/g, "\]")}
            const blob = new Blob([ response ], { type: "text/plain" });
            const url =  window.webkitURL.createObjectURL(blob);
            const name = (this as any).dataKeys[changeList] + (this as any).timestampToTime() + '.csv';
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

