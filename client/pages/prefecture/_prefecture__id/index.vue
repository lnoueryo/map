<template>
  <div>
    {{$route.params}}
    {{$store.getters['prefecture/addresses']}}
  </div>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  computed: {
    ...mapGetters('prefecture', [
      'cities',
      'addresses',
      'facilities',
      'occupations',
      'populations',
    ]),
    
  }
}
</script>