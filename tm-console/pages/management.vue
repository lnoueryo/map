<template>
  <div>
    <v-container fluid>
      <div>
        <top-bar></top-bar>
        <main-view ref="mainView"></main-view>
        <bottom-bar></bottom-bar>
      </div>
    </v-container>
    <modal></modal>
  </div>
</template>

<script lang="ts">
import Vue from 'vue';
const TopBar = () => import('../components/management/templates/TopBar.vue');
const MainView = () =>
  import('../components/management/templates/MainView.vue');
const BottomBar = () =>
  import('../components/management/templates/BottomBar.vue');
const Modal = () => import('../components/management/templates/Modal.vue');
interface DataType {
  open: boolean;
}
export default Vue.extend({
  components: {
    TopBar,
    MainView,
    BottomBar,
    Modal,
  },
  created() {
    this.$store.dispatch(
      'management/items',
      this.$store.getters['management/data']
    );
  },
});
</script>