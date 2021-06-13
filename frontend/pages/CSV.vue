<template>
    <div>
      {{convertTimeStamp}}
        <!-- <div style="background-color:white;height:100vh;width:100%;color:black">
            <div v-for="(company,i) in companies" :key="i">
                <span>{{company.name}}</span>
                <span>{{company.address}}</span>
                <span>{{company.founded}}</span>
            </div>
        </div> -->
  <v-container fluid>
    <v-data-iterator
      :items="items"
      :items-per-page.sync="itemsPerPage"
      :page.sync="page"
      :search="search"
      :sort-by="sortBy.toLowerCase()"
      :sort-desc="sortDesc"
      hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar
          dark
          color="blue darken-3"
          class="mb-1"
        >
          <v-text-field
            v-model="search"
            clearable
            flat
            solo-inverted
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
          ></v-text-field>
          <template v-if="$vuetify.breakpoint.mdAndUp">
            <v-spacer></v-spacer>
            <v-select
              v-model="sortBy"
              flat
              solo-inverted
              hide-details
              :items="keys"
              prepend-inner-icon="mdi-magnify"
              label="Sort by"
            ></v-select>
            <v-spacer></v-spacer>
            <v-btn-toggle
              v-model="sortDesc"
              mandatory
            >
              <v-btn
                large
                depressed
                color="blue"
                :value="false"
              >
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn
                large
                depressed
                color="blue"
                :value="true"
              >
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-toolbar>
      </template>

      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="item in props.items"
            :key="item.id"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold">
                {{ item.name }}
              </v-card-title>

              <v-divider></v-divider>

              <v-list dense>
                <v-list-item
                  v-for="(key, index) in filteredKeys"
                  :key="index"
                >
                  <v-list-item-content :class="{ 'blue--text': sortBy === key }">
                    {{ key }}:
                  </v-list-item-content>
                  <v-list-item-content
                    class="align-end"
                    :class="{ 'blue--text': sortBy === key }"
                  >
                    {{ item[key.toLowerCase()] }}
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <template v-slot:footer>
        <v-row
          class="mt-2"
          align="center"
          justify="center"
        >
          <span class="grey--text">Items per page</span>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                dark
                text
                color="primary"
                class="ml-2"
                v-bind="attrs"
                v-on="on"
              >
                {{ itemsPerPage }}
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(number, index) in itemsPerPageArray"
                :key="index"
                @click="updateItemsPerPage(number)"
              >
                <v-list-item-title>{{ number }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <v-spacer></v-spacer>

          <span
            class="mr-4
            grey--text"
          >
            Page {{ page }} of {{ numberOfPages }}
          </span>
          <v-btn
            fab
            dark
            color="blue darken-3"
            class="mr-1"
            @click="formerPage"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn
            fab
            dark
            color="blue darken-3"
            class="ml-1"
            @click="nextPage"
          >
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
    </div>
</template>
<script>
  export default {
    data () {
      return {
        itemsPerPageArray: [4, 8, 12],
        search: '',
        filter: {},
        sortDesc: false,
        page: 1,
        itemsPerPage: 4,
        sortBy: 'ID',
        keys: [
          'ID',
          'NAME',
          'ADDRESS',
          'FOUNDED',
          'CREATED_AT',
          'UPDATED_AT',
        ],
        items: [],
      }
    },
    computed: {
      numberOfPages () {
        return Math.ceil(this.items.length / this.itemsPerPage)
      },
      filteredKeys () {
        return this.keys.filter(key => key !== 'ID')
      },
      convertTimeStamp(){
        return this.items.map((item)=>{return new Date(item.created_at)})
      }
    },
    async created(){
      const response = await this.$axios.$get('/api/management/company/');
      this.items = response;
    },
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