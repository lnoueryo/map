<template>
    <div>
        <v-navigation-drawer v-model="drawer" :mini-variant="miniVariant" :clipped="clipped" width="300" fixed app>
            <v-list class="drawer-top">
                <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" router exact @click.stop="drawer = !drawer">
                <v-list-item-action>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title v-text="item.title" />
                </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <!-- <v-app-bar :clipped-left="clipped" :clipped-right="clipped" fixed app>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
            <v-toolbar-title v-text="title" />
            <v-spacer />
        </v-app-bar> -->
        <header id="header-bar">
            <div style="align-items:center;display:flex;">
                <v-btn icon class="mr-2" @click.stop="drawer = !drawer"><v-icon>mdi-menu</v-icon></v-btn>
                <router-link to="/" style="color:white;text-decoration:none;font-size:18px;font-weight:bold;">Map</router-link>
            </div>
            <!-- <div>
                <v-btn @click="refresh" color="orange">refresh</v-btn>
            </div> -->
        </header>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    data() {
        return {
            clipped: true,
            drawer: false,
            fixed: true,
            items: [
                {
                    icon: 'mdi-apps',
                    title: 'Home',
                    to: '/',
                },
                {
                    icon: 'mdi-apps',
                    title: 'Spot',
                    to: '/spot',
                },
                {
                    icon: 'mdi-apps',
                    title: 'Station',
                    to: '/station',
                },
                {
                    icon: 'mdi-apps',
                    title: 'Prefecture',
                    to: '/prefecture',
                },
                // {
                //     icon: 'mdi-chart-bubble',
                //     title: 'Login',
                //     to: '/login',
                // },
                // {
                //     icon: 'mdi-chart-bubble',
                //     title: 'admin',
                //     to: '/management',
                // },
                // {
                //     icon: 'mdi-chart-bubble',
                //     title: 'map',
                //     to: '/editmap',
                // },
            ],
            miniVariant: false,
            right: true,
            rightDrawer: false,
        }
    },
    computed:{
        filterItems(){
            return this.$data.items.filter((_: any, i: number)=>{return i == 0})
        }
    },
    methods:{
        async refresh(){
            const token = localStorage.getItem('token');
            const parsedToken = JSON.parse(token as string)
            const response = await this.$axios.$post('/api/token/refresh/', {refresh: parsedToken.refresh});
            this.$axios.setToken(response.access, 'Bearer')
        },
    }
})
</script>

<style lang="scss">
    #header-bar {
        height: 64px;
        background-color: #272727;
        padding: 0 10px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 5;
        align-items: center;
        display: flex;
        justify-content: space-between;
    }
    .drawer-top {
        padding-top: 64px!important;
    }
    @media screen and (max-width:768px) { 
        .drawer-top {
            padding-top: 0px!important;
        }
    }
</style>