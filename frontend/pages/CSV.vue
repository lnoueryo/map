<template>
    <div>
      <v-container fluid>
        <v-data-iterator :items="items" :items-per-page.sync="itemsPerPage" :page.sync="page" :search="search" :sort-by="sortBy.toLowerCase()" :sort-desc="sortDesc" hide-default-footer>
          <template v-slot:header>
            <v-toolbar dark color="blue darken-3" class="mb-1">
              <v-select v-model="data" flat solo-inverted hide-details :items="dataKeys" prepend-inner-icon="mdi-magnify" label="data"></v-select>
              <template v-if="$vuetify.breakpoint.mdAndUp">
                <v-spacer></v-spacer>
                <v-text-field v-model="search" clearable flat solo-inverted hide-details prepend-inner-icon="mdi-magnify" label="Search"></v-text-field>
                <v-spacer></v-spacer>
                <v-btn-toggle v-model="sortDesc" mandatory>
                  <v-btn large depressed color="blue" :value="false">
                    <v-icon>mdi-arrow-up</v-icon>
                  </v-btn>
                  <v-btn large depressed color="blue" :value="true">
                    <v-icon>mdi-arrow-down</v-icon>
                  </v-btn>
                </v-btn-toggle>
                <v-spacer></v-spacer>
                <v-select v-model="sortBy" flat solo-inverted hide-details :items="sortKeys" prepend-inner-icon="mdi-magnify" label="Sort by"></v-select>
              </template>
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
                <!-- <div v-model="editItem" :is="component"></div> -->
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
    </v-row>
    </div>
</template>
<script>
import Company from '~/components/management/Company.vue'
import Line from '~/components/management/Line.vue'
import Station from '~/components/management/Station.vue'
import { mapGetters } from 'vuex'
  export default {
    components:{
      Company,
      'train-line': Line,
      Station
    },
    data () {
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
      }
    },
    computed: {
      ...mapGetters('management', [
        'changeList',
        'sortKeys',
        'items',
      ]),
      numberOfPages () {
        return Math.ceil(this.items.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.sortKeys.filter(key => key !== 'ID')
      },
      component(){
          return this.componentTypes[this.changeList];
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
    // created(){
    //   this.$store.dispatch('management/items', this.$store.getters['management/data'])
    // },
    methods: {
      nextPage () {
        if (this.page + 1 <= this.numberOfPages) this.page += 1
      },
      formerPage () {
        if (this.page - 1 >= 1) this.page -= 1
      },
      updateItemsPerPage (number) {
        this.itemsPerPage = number
      },
      omittedContent(string) {
        const MAX_LENGTH = 30;
        if (string && string.length > MAX_LENGTH) {
          return string.substr(0, MAX_LENGTH) + '...';
        }
        return string;
      },
      edit(index){
        this.editDialog = true;
        this.$store.dispatch('management/editIndex', index)
      }
    },
  }
</script>
<!--<script lang="ts">
// import Vue from 'vue';
// export default Vue.extend({
//     data() {
//         return {
//             map: null,
//             overview: null,
//             companies: [],
//             csvData: null,
//             files: null,
//             table: 0,
//             delimiter: ',',
//             csv: null
//         }
//     },
//     async created(){
//         const response = await this.$axios.$get('/api/management/company/');
//         this.companies = response;
//     },
//     // async mounted(){
//     //     const response = await this.$axios.$get('/api/map/');
//     //     this.company = response;
//     // },
//     methods:{
//         clamp(num: number, min: number, max: number) {
//             return Math.min(Math.max(num, min), max);
//         },
//         getFiles(e){
//             // console.log(e.target.files[0]
//             this.files = e.target.files[0];
//             // const file = e.target.files[0];
//             // const reader = new FileReader();
//             // reader.onload=(e)=>{
//             //     this.csvData = e.target.result;
//             // }
//             // reader.readAsDataURL(file);
//         },
//         async sendCSV(){
//             // const response = this.$axios.$post('/api/map/csv/', {csv: this.csvData});
//             var formData = new FormData();
//             console.log(this.files)
//             formData.append("file", this.files);
//             this.$axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
//             this.$axios.defaults.xsrfCookieName = "csrftoken";
//             this.$axios.$post('/api/map/csv/', formData, {
//                 headers: {
//                 'Content-Type': 'multipart/form-data'
//                 }
//             })
//         },
//         async getCSV(){
//             const response = await this.$axios.$get('/api/map/csv/', {params: {table: this.table, delimiter: this.delimiter}});
//             var txt = "任意のテキスト";
//             var blob = new Blob([ response ], { type: "text/plain" });
//             this.csv = window.webkitURL.createObjectURL(blob);
//         },
//         async saveCompany(){
//             try {
//                 const response = await this.$axios.$post('/api/map/', {name: 'イノウエレイルウェイ', address: '東京都世田谷区松原1-43-14', founded: '1990年9月8日'});
//                 console.log(response)
//             } catch (error) {
//                 console.log(error.response)
//             }
//         }
//     }
// })
// </script>

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