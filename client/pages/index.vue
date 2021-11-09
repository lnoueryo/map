<template>
  <v-main>
    <v-container>
      <div class="d-flex flex-wrap">
        <v-card
          class="mx-auto my-12 card"
          v-for="(cardItem, i) in cardItems"
          :key="i"
          :to="cardItem.page"
          style="max-width: 350px;width:100%;"
        >

          <v-img
            height="250"
            :src="cardItem.image"
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
interface DataType {
  open: boolean;
  lefList: boolean;
  cardItems: {title: string, description: string, page: {name: string}, image: string}[]
}
export default Vue.extend({
  data(): DataType {
    return {
      open: false,
      lefList: false,
      cardItems: [
        {title: '観光地検索', description: '気になるロケーションの観光地を探そう', page: {name: 'spot'}, image: require('~/assets/img/spot-top.jpg')},
        {title: '駅検索', description: '駅とその周辺情報を調べよう', page: {name: 'station'}, image: require('~/assets/img/station-top.jpg')},
        {title: '都道府県情報', description: '都道府県情報を調べよう', page: {name: 'prefecture'}, image: require('~/assets/img/prefecture-top.jpg')},
      ]
    };
  },
  computed: {
    smp() {
      return this.$store.getters.windowSize.x < 500;
    },
  },
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
.card {
  transition: all .5s;
}
.card:hover {
  transition: all .5s;
  opacity: .5;
}
</style>