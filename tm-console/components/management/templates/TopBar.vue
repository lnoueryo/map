<template>
  <div>
    <v-toolbar dark color="blue darken-3" class="mb-1">
      <v-select
        v-model="data"
        flat
        solo-inverted
        hide-details
        :items="tableNames"
        prepend-inner-icon="mdi-magnify"
        label="data"
      ></v-select>
      <template v-if="$vuetify.breakpoint.mdAndUp">
        <v-spacer></v-spacer>
        <v-text-field
          v-model="search"
          clearable
          flat
          solo-inverted
          hide-details
          prepend-inner-icon="mdi-magnify"
          label="Search"
        ></v-text-field>
        <v-spacer></v-spacer>
        <v-select
          v-model="sortBy"
          flat
          solo-inverted
          hide-details
          :items="sortKeys"
          prepend-inner-icon="mdi-magnify"
          label="Sort by"
        ></v-select>
        <v-spacer></v-spacer>
        <v-btn-toggle v-model="sortDesc" mandatory>
          <v-btn large depressed color="blue" :value="false">
            <v-icon>mdi-arrow-up</v-icon>
          </v-btn>
          <v-btn large depressed color="blue" :value="true">
            <v-icon>mdi-arrow-down</v-icon>
          </v-btn>
        </v-btn-toggle>
      </template>
    </v-toolbar>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
  computed: {
    tableNames() {
      return this.$store.getters['tables'].map((table) => {
        if(table.name.endsWith('ies')) {
          return table.name.slice(0, -3) + 'y'
        }
        return table.name.slice(0, -1);
      }).filter((tableName) => tableName !== 'lines_station')
    },
    data: {
      get() {
        return this.$store.getters['management/data'];
      },
      set(value) {
        this.$store.dispatch('management/data', value);
      },
    },
    sortBy: {
      get() {
        return this.$store.getters['management/sortBy'];
      },
      set(value) {
        this.$store.dispatch('management/sortBy', value);
      },
    },
    sortDesc: {
      get() {
        return this.$store.getters['management/sortDesc'];
      },
      set(value) {
        this.$store.dispatch('management/sortDesc', value);
      },
    },
    search: {
      get() {
        return this.$store.getters['management/search'];
      },
      set(value) {
        this.$store.dispatch('management/search', value);
      },
    },
    sortKeys() {
      return this.$store.getters['management/sortKeys'];
    },
  },
  watch: {
    data: {
      async handler() {
        this.$store.dispatch(
          'management/items',
          this.$store.getters['management/data']
        );
      },
      immediate: false,
    },
  },
});
</script>
