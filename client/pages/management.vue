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
import Vue from 'vue'
import TopBar from '~/components/management/templates/TopBar.vue'
import MainView from '~/components/management/templates/MainView.vue'
import BottomBar from '~/components/management/templates/BottomBar.vue'
import Modal from '~/components/management/templates/Modal.vue'
interface DataType {open: boolean}
export default Vue.extend({
    components:{
        TopBar,
        MainView,
        BottomBar,
        Modal
    },
    beforeCreate(){
        this.$store.dispatch('management/items', this.$store.getters['management/data']);
    },
    mounted(){

    },
    methods:{
        drawer(){
            const mainView = this.$refs.mainView as InstanceType<typeof MainView>;
            mainView.$data.open=!mainView.$data.open;
        },
    }
})
</script>