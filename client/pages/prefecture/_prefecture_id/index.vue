<template>
  <div>
    <div v-if="prefecture">
      <div v-for="(city, i) in prefecture.cities" :key="i">
        <router-link :to="{name: 'prefecture-prefecture_id-city_code', params: {prefecture_id: city.prefecture_id, city_code: city.id}}">{{city.name}}</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  computed: {
    ...mapGetters('prefecture', [
      'prefectures',
      'cities',
    ]),
    prefecture() {
      return this.prefectures.find((prefecture) => {
        return prefecture.id == this.$route.params.prefecture_id;
      })
    }
  },
  created() {
    if(this.prefectures.length == 0) this.$store.dispatch('prefecture/getPrefectures', this.$route.params);
  }
}
</script>