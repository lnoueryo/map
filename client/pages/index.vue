<template>
  <v-main>
    <v-container>
      <div class="d-flex">
        <v-card
          class="mx-auto my-12"
          max-width="374"
          v-for="(cardItem, i) in cardItems"
          :key="i"
          :to="cardItem.page"
        >

          <v-img
            height="250"
            src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
          ></v-img>

          <v-card-title>{{cardItem.title}}</v-card-title>

          <v-card-text>

            <div class="text-subtitle-1">
              {{cardItem.description}}
            </div>

          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from "vue";
const LeftList = () => import("../components/index/templates/LeftList.vue");
const MapView = () => import("../components/index/templates/Map.vue");
interface DataType {
  open: boolean;
  lefList: boolean;
  cardItems: {title: string, description: string, page: {name: string}}[]
}
export default Vue.extend({
  components: {
    LeftList,
    MapView,
  },
  data(): DataType {
    return {
      open: false,
      lefList: false,
      cardItems: [
        {title: '観光地検索', description: '気になるロケーションの観光地を探そう', page: {name: 'spot'}},
        {title: '駅検索', description: '駅とその周辺情報を調べよう', page: {name: 'station'}},
      ]
    };
  },
  computed: {
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
  },
  // beforeCreate() {
  //     this.$store.dispatch('switch/getCompanies', ['stations, cities']);
  // },
  mounted() {
    this.$on("open", (this as any).drawer);
  },
  methods: {
    drawer() {
      //right-drawerが開いた時の処理
      (this as any).open = !(this as any).open;
    },
  },
});
</script>

<style lang="scss" scoped>
#wrapper {
  width: 100%;
  height: calc(100vh - 100px);
  position: relative;
  #container {
    width: 100%;
    position: relative;
    padding-right: 100px;
    transition: all 0.3s;
    .main-view {
      display: flex;
      overflow: hidden;
      .map-container {
        position: relative;
        width: 100%;
      }
    }
    @media screen and (max-width: 500px) {
      .main-view {
        //left-listを上げて、map-viewを下げる
        display: block;
      }
    }
  }
  #container.open {
    padding-right: 256px;
    transition: all 0.3s;
  }
  @media screen and (max-width: 500px) {
    #container {
      padding-right: 0;
    }
    #container.open {
      padding-right: 0;
      transition: all 0.3s;
    }
  }
}
</style>