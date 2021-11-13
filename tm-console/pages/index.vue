<template>
  <v-main>
    <v-container>
      <div class="d-flex flex-wrap justify-space-around" v-if="tables">
        <v-card class="my-3 card" max-width="344" v-for="(table, i) in tables" :key="i" :to="'/' + table.to">
          <v-card-text>
            <p class="text-h4 text--primary">
              {{table.name}}
            </p>
            <!-- <p>{{table.describe}}</p> -->
            <div class="d-flex">
              <div class="text--primary px-1" style="width: 50%" v-for="(columnArray, i) in table.columns" :key="i">
                <div v-for="(column, j) in columnArray" :key="j">
                  {{column}}
                </div>
              </div>
            </div>
          </v-card-text>
        </v-card>
        <v-card class="my-3" max-width="344" style="opacity: 0">
          <v-card-text>
            <p class="text-h4 text--primary">
              el·ee·mos·y·nar·y
            </p>
            <p>adjective</p>
            <div class="text--primary">
              relating to or dependent on charity; charitable.<br>
              "an eleemosynary educational institution."
            </div>
          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </v-main>
</template>

<script>
export default {
  data() {
    return {
      // tables: [
      //   {name: 'users', to: '/users', describe: 'ユーザー'},
      //   {name: 'prefectures', to: '/prefectures', describe: '都道府県'},
      //   {name: 'cities', to: '/cities', describe: '市区'},
      //   {name: 'spots', to: '/spots', describe: '観光地'},
      //   {name: 'companies', to: '/companies', describe: '鉄道会社'},
      //   {name: 'lines', to: '/lines', describe: '路線'},
      //   {name: 'stations', to: '/stations', describe: '駅'},
      //   {name: 'facilities', to: '/facilities', describe: '市区施設情報'},
      //   {name: 'occupations', to: '/occupations', describe: '市区職業情報'},
      //   {name: 'populations', to: '/populations', describe: '市区人口情報'},
      //   {name: 'towns', to: '/towns', describe: '町村'},
      // ]
    }
  },
  computed:{
    tables() {
      return this.$store.getters['tables'].length !== 0 ? this.$store.getters['tables'].filter((table) => {
        return table.name !== 'lines_stations';
      }) : null;
    }
  }
}
</script>

<style lang="scss">
  .card {
    min-width: 330px;
    transition: .5s;
    max-height: 370px;
    overflow: hidden;
  }
  .card:hover {
    opacity: .4;
    transition: .5s;
    cursor: pointer;
  }
</style>