<template>
    <div>
        <v-navigation-drawer v-model="drawer" :mini-variant="miniVariant" :clipped="clipped" width="300" fixed app>
            <v-list>
                <v-list-item v-for="(item, i) in items" :key="i" :to="item.to" router exact>
                <v-list-item-action>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title v-text="item.title" />
                </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-app-bar :clipped-left="clipped" :clipped-right="clipped" fixed app>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
            <v-toolbar-title v-text="title" />
            <v-spacer />
        </v-app-bar>
        <header style="height:64px;background-color: #272727;padding:0 10px;position:fixed;top:0;left:0;right:0;z-index:5;align-items:center;display:flex;">
            <div style="align-items:center;display:flex;">
                <v-btn icon class="mr-2" @click.stop="drawer = !drawer"><v-icon>mdi-menu</v-icon></v-btn>
                <router-link to="/" style="color:white;text-decoration:none;font-size:18px;font-weight:bold;">Map Pap</router-link>
            </div>
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
                    title: 'Welcome',
                    to: '/',
                },
                {
                    icon: 'mdi-chart-bubble',
                    title: 'Login',
                    to: '/login',
                },
            ],
            miniVariant: false,
            right: true,
            rightDrawer: false,
            title: 'Vuetify.js',
        }
    },
})
</script>