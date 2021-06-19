<template>
    <div>
        <v-container fluid>
            <div>
                <top-bar></top-bar>
                <main-view></main-view>
                <bottom-bar></bottom-bar>
            </div>
        </v-container>
        <modal></modal>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
import TopBar from '~/components/management/templates/TopBar.vue'
import MainView from '~/components/management/templates/MainView.vue'
import BottomBar from '~/components/management/templates/BottomBar.vue'
import Modal from '~/components/management/templates/Modal.vue'
export default Vue.extend({
    components:{
        TopBar,
        MainView,
        BottomBar,
        Modal
    },
})
</script>