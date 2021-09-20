<template>
  <div class="top">
    <div>
      <span v-for="(address, i) in addressElement" :key="i" class="px-1">{{
        address.Name
      }}</span>
    </div>
  </div>
</template>

<script>
import Vue from "vue";
export default Vue.extend({
  computed: {
    addressElement() {
      return this.$store.getters["station/addressElement"];
    },
  },
});
</script>

<style lang="scss">
.top {
  background-color: rgba(0, 0, 0, 0.5);
  width: 100%;
  padding: 0px 5%;
  height: 40px;
  display: flex;
  align-items: center;
}
</style>