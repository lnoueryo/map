<template>
  <v-main>
    <v-container>
      <div class="d-flex flex-wrap">
        <v-card
          class="mx-auto my-12"
          max-width="374"
          v-for="(prefecture, i) in prefectures"
          :key="i"
          :to="{name: 'prefecture-prefecture_id', params: {prefecture_id: prefecture.id}}"
        >

          <v-img
            height="250"
            :src="require(`~/assets/img/location/${prefecture.name}.jpg`)"
          ></v-img>

          <v-card-title>{{prefecture.name}}</v-card-title>

          <v-card-text>

            <div class="text-subtitle-1">
              <!-- {{cardItem.description}} -->
            </div>

          </v-card-text>
        </v-card>
      </div>
    </v-container>
  </v-main>
</template>

<script>
export default {
  computed: {
    prefectures() {
      return this.$store.getters['prefecture/prefectures'];
    }
  },
  created() {
    this.$store.dispatch('prefecture/getPrefectures');
  }
}
</script>