<template>
  <div>
    <v-content>
      <v-container>
        <v-main>
          <div v-if="prefecture">
            <div>
              <h1>{{ prefecture.name }}</h1>
            </div>
            <div class="d-flex flex-wrap">
              <div class="pa-4" v-for="(city, i) in prefecture.cities" :key="i">
                <router-link class="anchor" :to="{name: 'prefecture-prefecture_id-city_code', params: {prefecture_id: city.prefecture_id, city_code: city.id}}">
                  <h2 class="py-2 anchor">{{city.name}}</h2>
                </router-link>
              </div>
            </div>
          </div>
        </v-main>
      </v-container>
    </v-content>
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

<style lang="scss">
.anchor {
  text-decoration: none;
  color: white;
  transition: .5s;
}
.anchor:hover {
  opacity: 0.7;
  transition: .5s;
}
</style>