<template>
  <div>
    <v-content>
      <v-container>
        <v-main v-if="spotInfo">
          <div>
            <div v-if="!smp">
              <h2>{{ spotInfo.name }}</h2>
            </div>
          </div>
          <div class="d-flex flex-wrap" style="justify-content: space-around;">
            <map-view class="my-4" :stations="nearestStations"></map-view>
            <div v-if="smp">
              <h2>{{ spotInfo.name }}</h2>
            </div>
            <v-carousel class="my-4" hide-delimiters v-if="photos.length !== 0" style="max-width: 550px;" :height="smp?250:500">
                <v-carousel-item v-for="(item,i) in photos" :key="i" :src="item" style="max-width: 550px;"></v-carousel-item>
            </v-carousel>
          </div>
          <h3>詳細情報</h3>
          <div class="d-flex flex-wrap" style="justify-content: space-around;">
            <div class="my-4" style="max-width: 550px;width: 100%">
              <div class="mb-3">
                <h4 class="mb-1">住所</h4>
                <span>{{spotInfo.address}}</span>
              </div>
              <div class="mb-3">
                <h4 class="mb-1">最寄り駅</h4>
                <div class="pb-1" v-for="(station, i) in nearestStations" :key="i">
                  <div class="d-flex mb-2">
                    <div class="mr-2">
                      {{station.name}}
                    </div>
                    <div>
                      {{station.company.name}}
                    </div>
                  </div>
                  <div class="d-flex flex-wrap pb-2 py-2" style="font-size: 14px">
                    <div class="mr-2 mb-3 chip" :style="{backgroundColor: line.color}" v-for="(line, j) in station.lines" :key="j" @click="toStation(line, station.name)">
                      {{line.name}}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="my-4" style="max-width: 550px;width: 100%;">
              <h4 class="mb-1">周辺施設</h4>
              <div class="d-flex flex-wrap" style="font-size: 14px">
                <div class="py-1 px-4 mr-4 mb-4" :style="{backgroundColor: spot.color, borderRadius: '5px'}" v-for="(spot, i) in aroundSpotInfo" :key="i">
                  <div class="text-center">
                    <v-icon>mdi-{{spot.icon}}</v-icon>
                  </div>
                  <div>
                    {{spot.Name}}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="places my-4" v-if="placesData">
            <div class="reviews-container" v-if="placesData.reviews">
              <div class="reviews-top">
                <div class="average-score">{{placesData.rating}}</div>
                <span class="star5_rating" :data-rate="roundHalf(placesData.rating)"></span>
              </div>
              <div>
                <div class="review" v-for="(review, i) in placesData.reviews" :key="i">
                  <div class="d-flex mb-4">
                    <img class="avatar" :src="review.profile_photo_url">
                    <div class="rating-container">
                      <div>{{review.author_name}}</div>
                      <div>
                        <span class="star5_rating" :data-rate="review.rating"></span>
                        <span>{{review.relative_time_description}}</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <p class="review-comment">{{review.text}}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div>
            <div class="py-4" v-if="twitterInfo.length !== 0">
              <div class="d-flex">
                <v-icon class="mr-2" size="32" color="#1d9bf0">mdi-twitter</v-icon>
                <h2>Twitter</h2>
              </div>
              <div class="py-4" v-for="(twitter, i) in twitterInfo" :key="i">
                <div class="px-1" style="display: flex">
                  <div>
                    <img class="avator" :src="twitter.profile_image_url" />
                  </div>
                  <div class="px-1">
                    <div>{{ twitter.name }}</div>
                    <div style="color: #536471">{{ changeTime(twitter.created_at) }}</div>
                    <div class="py-1" style="font-size: 14px">
                      <span v-html="twitter.text"></span>
                    </div>
                  </div>
                </div>
                <div v-if="twitter.images.length !== 0">
                  <v-carousel
                    hide-delimiters
                    :show-arrows="twitter.images.length !== 1"
                    height="250px"
                  >
                    <v-carousel-item
                      v-for="(image, j) in twitter.images"
                      :key="j"
                      :src="image"
                      @click="dialogPhoto=image;dialog=true;"
                    ></v-carousel-item>
                  </v-carousel>
                </div>
              </div>
            </div>
          </div>
        </v-main>
      </v-container>
    </v-content>
    <v-dialog
      v-model="dialog"
      width="800"
    >
      <v-img :src="dialogPhoto" style="margin: auto;max-width: 800px;max-height: 400px" @click="dialog=false"></v-img>
    </v-dialog>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
const gh = require('ngeohash');
const MapView = () => import("~/components/detail/templates/Map.vue");
interface AroundSpotInfo { "Name": string, "Uid": string, "Category": string, "Label": string, "Combined": string}
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string, geohash: string, company: Company }
interface Company { id: number, name: string, address: string, founded: string, lines: Line[] };
interface Line { id: number, company_id: number, name: string, polygon: Polygon, color: string, stations: Station[] };
interface Polygon { lat: number, lng: number }[];
export default Vue.extend({
  data() {
    return {
      dialog: false,
      dialogPhoto: null,
      excludedArray: ['駅', '地点名', 'トンネル', '観光地', '道路名', '滝', '海', '川', '道路'],
      categoryArray: [
        {category: ['ホテル', '民宿', '旅館'], color: '#0079b3', icon: 'bed'},
        {category: ['レストラン', 'サイゼリヤ', 'マクドナルド', 'モスバーガー', 'フレッシュネスバーガー', '飲食', '松屋', 'すき家', 'CoCo壱番屋', '餃子の王将', '丸亀製麺', 'デニーズ', 'ロイヤルホスト', '吉野家'], color: '#00bae8', icon: 'silverware-fork-knife'},
        {category: ['ローソン', 'ファミリーマート', 'セブン-イレブン', 'ヤマザキデイリーストアー', 'コンビニ'], color: '#89d2e5', icon: 'store-24-hour'},
        {category: ['公園'], color: '#5ae7b3', icon: 'pine-tree'},
        {category: ['校', '学'], color: '#89e5d0', icon: 'school'},
        {category: ['図書館'], color: '#be69f3', icon: 'library'},
        {category: ['役所'], color: '#be69f3', icon: 'warehouse'},
        {category: ['信用金庫', '銀行'], color: '#be69f3', icon: 'bank'},
        {category: ['郵便'], color: '#be69f3', icon: 'mailbox'},
        {category: ['温泉'], color: '#0079b3', icon: 'bathtub'},
        {category: ['神社'], color: '#0079b3', icon: 'crosshairs-gps'},
        {category: ['書店'], color: '#00bae8', icon: 'book'},
        {category: ['警察'], color: '#be69f3', icon: 'car-emergency'},
        {category: ['消防'], color: '#be69f3', icon: 'fire-truck'},
        {category: ['病院'], color: '#be69f3', icon: 'hospital-box'},
        {category: ['エネオス', '出光', '昭和シェル石油', 'コスモ石油'], color: '#fd70b8', icon: 'gas-station'},
        {category: ['保育', '幼稚園'], color: '#89e5d0', icon: 'baby-face'},
      ],
      nameArray: [
        {category: ['公園'], color: '#5ae7b3', icon: 'pine-tree'},
      ]
    }
  },
  components: {
    MapView,
  },
  beforeCreate() {
    this.$store.dispatch('detail/params', this.$route.params);
  },
  computed: {
    spotInfo() {
      return this.$store.getters['detail/spotInfo'];
    },
    placesData() {
      return this.$store.getters['info/spotDetail'];
    },
    nearestStations() {
      const expandNeighborArea = this.expandNeighborArea((this as any).spotInfo.geohash)
      let nearestStations = this.$store.getters['detail/combineStationsWithLines'].filter((station: Station) => {
        return expandNeighborArea.includes(station.geohash);
      });
      if (nearestStations.length == 0) {
        nearestStations = this.$store.getters['detail/combineStationsWithLines'].filter((station: Station) => {
          return gh.neighbors((this as any).spotInfo.geohash.slice(0, -1)).includes(station.geohash.slice(0, -1));
        });
      }
      return nearestStations.map((station: Station) => {
        const company = this.$store.getters['detail/companies'].find((company: Company) => {
          return company.id == station.company_id;
        })
        station['company'] = company;
        return station;
      })
    },
    photos() {
        if ((this as any).placesData?.photos) {
            const photos = (this as any).placesData?.photos.map((photo: google.maps.places.PlacePhoto) => {
                return photo.getUrl();
            })
            return photos;
        }
        return [];
    },
    twitterInfo() {
      return this.$store.getters['info/twitterInfo']
    },
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
    aroundSpotInfo() {
      return this.$store.getters['info/aroundSpotInfo'].filter((spot: any) => {
        return this.excludedArray.some((key) => spot.Category.includes(key)) === false;
      }).filter((spot: any, index: number) => index < 14).map((spot) => {
        return this.addInfo(spot);
      });
    },
  },
  created() {
    this.$store.dispatch('info/getTwitterInfo', (this as any).spotInfo)
  },
  methods: {
    roundHalf(num: number) {
        return Math.round(num * 2) / 2;
    },
    changeTime(time: string) {
      let date = new Date(time);
      const year = date.getFullYear();
      const month = ("0" + (date.getMonth() + 1)).slice(-2);
      const day = ("0" + date.getDate()).slice(-2);
      const hours = ("0" + date.getHours()).slice(-2);
      const minutes = ("0" + date.getMinutes()).slice(-2);
      const changedDate = `${year}-${month}-${day} ${hours}:${minutes}`;
      return changedDate;
    },
    expandNeighborArea(geohash: string) {
      const neighbors = gh.neighbors(geohash)
      const expandedNeighbors = neighbors.map((neighbor: string[]) => gh.neighbors(neighbor));
      const uniqueExpandedNeighbors = Array.from(new Set(expandedNeighbors.flat()));
      return uniqueExpandedNeighbors;
    },
    toStation(line: Line, name: string) {
      this.$router.push({name: 'station-name', params: {name: name}, query: {company_id: String(line.company_id), line_id: String(line.id)}})
    },
    addInfo(spot) {
      const name = spot.Name;
      const category = spot.Category;
      let spotAddInfo = this.nameArray.find((nameInfo) => {
        return nameInfo.category.some((key) => name.includes(key));
      })
      spotAddInfo = this.categoryArray.find((spotInfo) => {
        return spotInfo.category.some((key) => category.includes(key));
      }) ?? spotAddInfo
      console.log(spotAddInfo)
      if(spot.Name.indexOf('店') > -1) Object.assign(spot, {category: '', color: '#be69f3', icon: 'store'})
      if('icon' in spot === false) Object.assign(spot, {category: '', color: '#be69f3', icon: 'square-medium'})
      console.log(spot)
      return spotAddInfo ? Object.assign(spot, spotAddInfo) : spot;
    }
  }
});
</script>

<style lang="scss" scoped>
.map-container {
  position: relative;
  width: 100%;
  max-width: 550px;
  // height: 100vh;
  // max-height: calc(var(--vh, 1vh) * 100 - 64px);
  #map {
    width: 100%;
    height: 100%;
    position: relative;
    padding-top: 56.25%;
    transition: all 0.5s;
  }
}
.reviews-container {
  padding: 10px;
  // background-color: #f7f7f7;
  width: 100%;
  border-radius: 5px;
}
.places {
  max-width: 1160px;
  // color: black;
  display: flex;
  justify-content: center;
}
/* レビュー */
.reviews-top {
  display: flex;
  align-items: baseline;
  p {
    margin-left: 5px;
  }
  .average-score {
    font-size: 37px;
    font-weight: bold;
  }
  .star5_rating {
    margin-left: 15px;
  }
}
.review {
  margin: 20px 0;
  .review-comment {
    font-size: 14px;
  }
}
.d-flex {
  display: flex;
}
.avatar {
  width: 48px;
  height: 48px;
}
.rating-container {
  margin-left: 10px;
  font-size: 15px;
}
.chip {
  padding: 0 8px;
  border-radius: 10px;
  cursor: pointer;
  transition: all .5s;
}
.chip:hover {
  opacity: .8
}
.chip:active {
  opacity: .9
}
/* レート */
.star5_rating {
  position: relative;
  z-index: 0;
  display: inline-block;
  white-space: nowrap;
  margin-right: 10px;
  color: #CCCCCC;
}
.star5_rating:before, .star5_rating:after {
  content: '★★★★★';
}
.star5_rating:after {
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  overflow: hidden;
  white-space: nowrap;
  color: #ffcf32;
}
/* 星5 */
.star5_rating[data-rate="5"]:after {
  width: 100%;
}
/* 星4.5 */
.star5_rating[data-rate="4.5"]:after {
  width: 90%;
}
/* 星4 */
.star5_rating[data-rate="4"]:after {
  width: 80%;
}
/* 星3.5 */
.star5_rating[data-rate="3.5"]:after {
  width: 70%;
}
/* 星3 */
.star5_rating[data-rate="3"]:after {
  width: 60%;
}
/* 星2.5 */
.star5_rating[data-rate="2.5"]:after {
  width: 50%;
}
/* 星2 */
.star5_rating[data-rate="2"]:after {
  width: 40%;
}
/* 星1.5 */
.star5_rating[data-rate="1.5"]:after {
  width: 30%;
}
/* 星1 */
.star5_rating[data-rate="1"]:after {
  width: 20%;
}
/* 星0.5 */
.star5_rating[data-rate="0.5"]:after {
  width: 10%;
}
/* 星0 */
.star5_rating[data-rate="0"]:after {
  width: 0%;
}
</style>