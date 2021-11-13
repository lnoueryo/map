<template>
  <div>
    <div class="d-flex">
      <v-row>
        <v-col
          v-for="(item, i) in filterByWord"
          :key="i"
          cols="12"
          sm="6"
          md="4"
          lg="3"
        >
          <v-card>
            <v-card-title
              class="subheading font-weight-bold d-flex"
              style="justify-content: space-between"
            >
              <div>{{ item.name }}</div>
              <div><v-btn color="orange" @click="edit(i)">編集</v-btn></div>
            </v-card-title>

            <v-divider></v-divider>

            <v-list dense>
              <v-list-item v-for="(key, j) in filteredKeys" :key="j">
                <v-list-item-content :class="{ 'blue--text': sortBy === key }">
                  {{ key }}:
                </v-list-item-content>
                <v-list-item-content
                  class="align-end"
                  :class="{ 'blue--text': sortBy === key }"
                >
                  {{ omittedContent(item[key.toLowerCase()]) }}
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
      <div>
        <div
          class="animation"
          :class="{ 'animation-open': open }"
          ref="drawer"
        ></div>
        <div class="drawer" :class="{ 'drawer-open': open }"></div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
interface DataType {
  filter: {};
  page: number;
  open: boolean;
}
import { mapGetters } from "vuex";
export default Vue.extend({
  data(): DataType {
    return {
      open: false,
      filter: {},
      page: 1,
    };
  },
  computed: {
    ...mapGetters('management', [
      'changeList',
      'sortKeys',
      'sortBy',
      'filterByKey',
      'filterByWord',
      'itemsPerPage',
      'itemsPerPageArray',
    ]),
    numberOfPages() {
      return Math.ceil(this.filterByWord.length / (this as any).itemsPerPage);
    },
    filteredKeys() {
      return this.sortKeys.filter((key: string) => key !== "ID");
    },
    component() {
      return (this as any).componentTypes[this.changeList];
    },
    selectedItem: {
      get() {
        return this.$store.getters['management/selectedItem'];
      },
      set(value) {
        this.$store.dispatch('management/selectedItem', value);
      },
    },
    itemsPerPage: {
      get() {
        return this.$store.getters['management/itemsPerPage'];
      },
      set(value) {
        this.$store.dispatch('management/itemsPerPage', value);
      },
    },
  },
  created() {
    this.$store.dispatch(
      'management/items',
      this.$store.getters['management/data']
    );
  },
  methods: {
    nextPage() {
      if ((this as any).page + 1 <= (this as any).numberOfPages)
        (this as any).page += 1;
    },
    formerPage() {
      if ((this as any).page - 1 >= 1) (this as any).page -= 1;
    },
    updateItemsPerPage(number: number) {
      (this as any).itemsPerPage = number;
    },
    omittedContent(string: string) {
      const MAX_LENGTH = 50;
      if (Array.isArray(string)) {
        string = JSON.stringify(string);
      }
      if (string && string.length > MAX_LENGTH) {
        return string.substr(0, MAX_LENGTH) + "...";
      }
      return string;
    },
    edit(index: number) {
      this.$store.dispatch('management/editIndex', index);
    },
  },
});
</script>

<style lang="scss">
.animation {
  width: 0;
  transform: translateX(50px);
  transition: all 0.3s;
}
.animation-open {
  width: 280px;
}
.drawer {
  width: 280px;
  right: -280px;
  position: fixed;
  transition: all 0.3s;
  padding: 15px;
}
.drawer-open {
  right: 12px;
}
</style>