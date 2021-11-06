<template>
  <div>
    <v-container>
      <v-main v-if="Object.keys(city).length !== 0">
        <div>
            <h1>{{ city.name }}</h1>
          <div class="d-flex justify-space-between align-center py-2">
          </div>
          <h2 class="py-2">基本情報</h2>
          <v-card>
            <div class="d-flex tabs">
              <h2 class="tab" :class="{'active': tabsKey == 0}" @click="tabsKey = 0">人口</h2>
              <h2 class="tab" :class="{'active': tabsKey == 1}" @click="tabsKey = 1">職業</h2>
              <h2 class="tab" :class="{'active': tabsKey == 2}" @click="tabsKey = 2">施設</h2>
            </div>
            <div class="content">
              <transition name="fade" mode="out-in">
                <tabs :tabItems="populationItems" :tabValues="city.population" unit="人" v-if="tabsKey == 0 && city.population" key="0"></tabs>
                <tabs :tabItems="occupationItems" :tabValues="city.occupation" unit="人" v-if="tabsKey == 1" key="1"></tabs>
                <tabs :tabItems="facilityItems" :tabValues="city.facility" unit="件" v-if="tabsKey == 2" key="2"></tabs>
              </transition>
            </div>
          </v-card>
          <div v-if="city.columns.length !== 0">
            <h2 class="py-2">賃貸</h2>
            <div>
              <div class="price-title">
                <h2>{{city.name}}全体の賃貸価格</h2>
                <div class="ac-content">
                  <city :analysisData="city"></city>
                </div>
              </div>
            </div>
          </div>
          <div class="price-title" v-if="city.layouts.length !== 0">
            <h2 class="pointer" @click="layoutSwitch = !layoutSwitch">
              <span>間取り別賃貸価格</span>
              <v-btn icon absolute right>
                <v-icon large :style="layoutSwitch ? {transform: 'rotate(180deg)'} : {transform: 'rotate(0deg)'}">mdi-menu-down</v-icon>
              </v-btn>
            </h2>
            <div class="ac-content">
              <div :style="layoutSwitch ? {maxHeight: '100%', height: `${$refs.layout.$el.getBoundingClientRect().height}px`, transition: 'all 1s'} : {height: 0, transition: 'all 1s'}">
                <layout ref="layout" :analysisData="city"></layout>
              </div>
            </div>
          </div>
          <div class="price-title" v-if="city.towns.length !== 0">
            <h2 class="pointer" @click="addressSwitch = !addressSwitch">
              <span>町別賃貸価格</span>
              <v-btn icon absolute right>
                <v-icon large :style="addressSwitch ? {transform: 'rotate(180deg)'} : {transform: 'rotate(0deg)'}">mdi-menu-down</v-icon>
              </v-btn>
            </h2>
            <div class="ac-content">
              <div :style="addressSwitch ? {maxHeight: '100%', height: `${$refs.town.$el.getBoundingClientRect().height}px`, transition: 'all 1s'} : {height: 0, transition: 'all 1s'}">
                <town ref="town" :analysisData="city"></town>
              </div>
            </div>
          </div>
          <h2 class="py-2">観光地</h2>
          <div class="price-title">
            <div class="pa-4" v-for="(spot, i) in city.spots" :key="i">
              <router-link class="d-flex anchor" :to="{name: 'spot-detail-prefecture_id-city_code-id', params: {prefecture_id: spot.prefecture_id, city_code: spot.city_code, id: spot.id}}">
              <div>{{spot.name}}:　</div>
              <div>{{spot.address}}</div>
              </router-link>
            </div>
          </div>
          <h2 class="py-2">駅</h2>
          <div class="price-title">
            <div class="pa-4" v-for="(company, i) in companies" :key="i">
              <h4 class="text-left">{{company.name}}</h4>
              <div class="d-flex flex-wrap">
                <div class="py-2 pr-2" v-for="(station, j) in company.stations" :key="j">
                  <div>
                    <router-link class="anchor" :to="{name: 'station-prefecture_id-name-detail-company_id', params: {prefecture_id: station.prefecture_id, name: station.name, company_id: company.id}}">{{station.name}}</router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </v-main>
    </v-container>
    <!-- <v-dialog
      v-model="dialog"
      width="800"
    >
      <v-img :src="dialogPhoto" style="margin: auto;max-width: 800px;max-height: 400px" @click="dialog=false"></v-img>
    </v-dialog> -->
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
// import analysisData from '~/assets/json/analyzed_column_json/13.json'
const Tabs = () => import('~/components/prefecture/template/Tabs.vue');
const Town = () => import('~/components/prefecture/template/Town.vue');
const Layout = () => import('~/components/prefecture/template/Layout.vue');
const City = () => import('~/components/prefecture/template/City.vue');
export default {
  components: {
    Tabs,
    Town,
    Layout,
    City
  },
  data() {
    return {
      layoutSwitch: false,
      addressSwitch: false,
      tabsKey: 0,
    }
  },
  computed: {
    ...mapGetters('prefecture', [
      'city',
    ]),
    companies() {
      console.log(Object.keys(this.city).length !== 0)
      if(Object.keys(this.city).length !== 0) {
        const city = JSON.parse(JSON.stringify(this.city))
        const overlappedCompanies = city.stations.map((station) => {
          return station.company;
        });
        const map = new Map(overlappedCompanies.map(overlappedCompany => [overlappedCompany.id, overlappedCompany]));
        let companies = Array.from(map.values());
        companies = companies.map((company) => {
          company['stations'] = city.stations.filter((station) => {
            delete station['company']
            return company.id == station.company_id;
          })
          return company
        })
        return companies || []
      }
    },
    // combineCompaniesWithStations() {
    //   const companies = JSON.parse(JSON.stringify(this.companies))
    //   return companies.map((company) => {
    //     company['stations'] = this.stations.filter((station) => {
    //       return station.city_code == this.$route.params.city_code && company.id == station.company_id;
    //     })
    //     return company
    //   }).filter((company) => company.stations.length !== 0)
    // },
    prefectureId() {
      return this.$route.params.prefecture_id;
    },
    cityCode() {
      return this.$route.params.city_code;
    },
    columnItems() {
      return [
        {title: '平均', value: 'mean'},
        {title: '中央値', value: '50%'},
        {title: '標準偏差', value: 'std'},
        {title: '最小値', value: 'min'},
        {title: '最大値', value: 'max'}
      ]
    },
    populationItems() {
      return [
        {title: '人口', value: 'population'},
        {title: '日本人', value: 'japanese'},
        {title: '外国人', value: 'foreign'},
        {title: '住民基本台帳人口', value: 'basic_resident_register_population'},
        {title: '14歳以下', value: 'under15'},
        {title: '15歳以上64歳以下', value: 'between15_64'},
        {title: '65歳以上', value: 'over65'},
        {title: '昼間人口', value: 'daytime'},
        {title: '年間出生数', value: 'births'},
        {title: '年間死者数', value: 'death'},
        {title: '総世帯数', value: 'total_households'},
        {title: '2人以上の世帯', value: 'nuclear_family_households'},
        {title: '単身世帯', value: 'single_households'},
        {title: '転入者', value: 'transferees'},
        {title: '転出者', value: 'mover'},
        {title: '年間婚姻数', value: 'marriages'},
        {title: '年間離婚数', value: 'divorces'},
        {title: '総面積', value: 'area'},
        {title: '可住地面積', value: 'area'},
      ]
    },
    occupationItems() {
      return [
        {title: '納税者', value: 'taxpayers'},
        {title: '事業所数', value: 'offices'},
        {title: '幼稚園の教員', value: 'kindergartener'},
        {title: '小学校の先生', value: 'elementary_school_teacher'},
        {title: '小学校の生徒', value: 'elementary_school_student'},
        {title: '中学校の先生', value: 'junior_high_school_teacher'},
        {title: '中学校の生徒', value: 'junior_high_school_student'},
        {title: '労働力人口 ', value: 'working_age_population'},
        {title: '就業者数', value: 'employed_population'},
        {title: '完全失業者数', value: 'unemployed_population'},
        {title: '役員', value: 'executive_officer'},
        {title: '雇い主', value: 'owners'},
        {title: '個人事業主', value: 'self_employed'},
        {title: '家族従業者', value: 'family_employees'},
        {title: '自市区町村の就業者', value: 'workers_in_your_city'},
        {title: '他市区町村の通勤者', value: 'workers_in_another_city'},
        {title: '従業地による就業者', value: 'employees_working_in_office'},
        {title: '他市区町村からの通勤者', value: 'commuting_population_from_other_city'},
        {title: '医者', value: 'doctor'},
        {title: '歯医者', value: 'dentist'},
        {title: '薬剤師', value: 'pharmacist'},
      ]
    },
    facilityItems() {
      return [
        {title: '公民館', value: 'community_center'},
        {title: '図書館', value: 'library'},
        {title: '家', value: 'house'},
        {title: '１住宅当たりの面積', value: 'occupation_area'},
        {title: '小売店', value: 'shop'},
        {title: '飲食店', value: 'restaurant'},
        {title: '大型小売店', value: 'store'},
        {title: 'スーパーマーケット ', value: 'supermarket'},
        {title: '病院', value: 'supermarket'},
        {title: '診療所', value: 'clinic'},
        {title: '歯科医院', value: 'dental_clinic'},
        {title: '介護施設', value: 'nursing_facility'},
        {title: '孤児院', value: 'orphanage'},
        {title: '保育所', value: 'nursery_center'},
        {title: '幼稚園', value: 'kindergarten'},
        {title: '小学校', value: 'elementary_school'},
        {title: '中学校', value: 'junior_high_school'},
        {title: '高校', value: 'high_school'},
      ]
    },
    units(){
      return ['円', '年', '㎡']
    },
    tabUnits(){
      return ['人', '人', '件']
    },
    selectedAddress() {
      return this.city.towns;
    },
    facility() {
      return this.city.facilities;
    },
    occupation() {
      return this.city.occupations
    },
    population() {
      return this.city.populations;
    },
    tabValues() {
      return [this.population, this.occupation, this.facility]
    },
    tabItems() {
      return [this.populationItems, this.occupationItems, this.facilityItems]
    },
    stations() {
      return this.city.stations;
    },
    smp() {
      return this.$store.getters.windowSize.x < 500
    },
    tablet() {
      return this.$store.getters.windowSize.x < 768
    },
  },
  watch: {
    layoutSwitch() {
      console.log(this.$refs.layout.$el.getBoundingClientRect())
    }
  },
  created() {
    this.$store.dispatch('prefecture/getCity', this.$route.params)
  },
  methods: {
    round(num) {
      return Math.round(num*100) / 100
    },
    roundPercentage(num) {
      return Math.round(num*10000) / 100
    },
    roundPrice(num) {
      return Math.round(num / 100) / 100;
    },
    page(num) {
      const city_code = Number(this.$route.params.city_code) + num;
      // this.$router.push({name: 'station-name', params: {name: '飯田橋駅'}})
      // this.$router.push({name: 'prefecture-prefecture_id-city_code', params: {prefecture_id: '13', city_code: String(city_code)}})
      this.$router.push({name: 'prefecture-prefecture__id-city_code', params: {prefecture__id: '13', city_code: String(city_code)}})
    }
  }
}
</script>

<style lang="scss" scoped>
  .anchor {
    text-decoration: none;
    color: white;
  }
  .tabs {
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    width: 100%;
    justify-content: space-between;
    outline: none;
    text-align: center;
    transition: all .2s;
  }
  .tab {
    background-color: #6a6a6a;
    width: 33%;
    border-radius: 5px 5px 0 0;
    outline: none;
    cursor: pointer;
  }
  .active {
    background-color: #484848;
    outline: none;
    transition: all .2s;
  }
  .content {
    border-top: solid 2px #484848;
    background-color: #484848;
  }
  .price-title {
    text-align: center;
    padding: 25px 20px;
    background-color: #484848;
    margin: 10px 0 0;
    border-radius: 5px;
  }
  .ac-content {
    overflow: hidden;
    background-color: #484848;
  }
  .pointer {
    cursor: pointer;
  }
  .table-row {
    display: flex;
    align-items: center;
  }
  .town-name {
    width: 15%;
  }
  .columns {
    width: 85%;
  }
  .table-data {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 16px;
  }
  .property {
    width: 15%;
  }
  .column {
    width: 12.25%;
  }
  @media screen and (max-width: 768px) {
    .table-row {
      display: block;
    }
    .town-name {
      width: 100%;
    }
    .columns {
      width: 100%;
      display: flex;
      justify-content: space-around;
    }
    .table-data {
      display: block;
      width: 25%;
      padding: 4px;
    }
    .property {
      width: 100%;
      display: flex;
      justify-content: center;
    }
    .column {
      width: 100%;
      max-height: 24px;
      overflow: hidden;
    }
  }
  .fade-enter-active,
  .fade-leave-active {
    transition: opacity 0.2s;
  }
  .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
    opacity: 0;
    transition: opacity 0.2s;
  }
</style>
大まかに言うと、事業所は拠点数（本社、支社、支店、営業所もそれぞれ一つと数える。営利、非営利を問わない。学校や病院、役場も含まれる。）、企業は法人（株式会社、有限会社、協同組合などの数）と個人の両方、会社は株式会社、合同会社などの営利法人会社を言います。
非営利の役所や公立学校などをを「公営」、それ以外を「民営」として区分しています。
これらの数値は事業所統計（五年毎に実施）による数値です。