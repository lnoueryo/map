<template>
    <div>
        <nav class="bottom-bar" :style="navStyle">
            <div class="hidden-frame">
                <div class="d-flex" v-if="show">
                    <div class="mx-2 w100">
                        <v-btn block @click="upWiki" v-if="!position">up</v-btn>
                        <v-btn block @click="downWiki" v-else>down</v-btn>
                    </div>
                    <div class="mx-2 w100">
                        <v-btn block @click="fade">delete</v-btn>
                    </div>
                </div>
                <div :style="componentStyle">
                    <slot></slot>
                </div>
            </div>
        </nav>
    </div>
</template>

<script>
export default {
    props: ['show'],
    data() {
        return {
            translateY: 0,
            navStyle: {
                height: 0,
                transform: '',
                transition: 'all .5s',
                zIndex: 0,
            },
            componentStyle: {
                height: 0,
                transition: 'all .5s',
                overflowY: 'hidden',
                overflowX: 'hidden',
            },
            position: false,
        }
    },
    computed: {
        transform() {
            return {transform: `translateY(${this.translateY}px)`, transition: 'all .5s'};
        },
    },
    watch:{
        show: {
            handler(v) {
                if (v) {
                    const newNavStyle = {height: '100px', transform: 'translateY(-100px)'};
                    const newComponentStyle = {height: '40px'};
                    this.navStyle = {...this.navStyle, ...newNavStyle};
                    this.componentStyle = {...this.componentStyle, ...newComponentStyle};
                }
            }
        }
    },
    methods:{
        upWiki() {
            this.position = true;
            const newNavStyle = {height: '100vh', transform: `translateY(-100vh)`, zIndex: 10};
            const newComponentStyle = {height: 'calc(100vh - 40px)', overflowY: 'scroll'};
            this.navStyle = {...this.navStyle, ...newNavStyle};
            this.componentStyle = {...this.componentStyle, ...newComponentStyle};
        },
        downWiki() {
            this.position = false;
            const newNavStyle = {height: '100px', transform: 'translateY(-100px)', zIndex: 0};
            const newComponentStyle = {height: '40px', overflowY: 'hidden'};
            this.navStyle = {...this.navStyle, ...newNavStyle};
            this.componentStyle = {...this.componentStyle, ...newComponentStyle};
        },
        fade() {
            this.$emit('hide');
            this.position = false;
            const newNavStyle = {height: '0px', transform: 'translateY(0px)', zIndex: 0};
            const newComponentStyle = {height: '0px', overflowY: 'hidden'};
            this.navStyle = {...this.navStyle, ...newNavStyle};
            this.componentStyle = {...this.componentStyle, ...newComponentStyle};
        }
    }
}
</script>

<style lang="scss" scoped>
    .bottom-bar {
        position: absolute;
        right: 0;
        left: 0;
        color: black;
        background-color: #ffffff;
    }
    .mw-parser-output {
        position: relative;
        z-index: 10;
        background-color: white;
        margin: auto;
    }
    .hidden-frame {
        overflow-x: hidden;
        width: 100%;
    }
    .w100 {
        width: 100%;
    }
</style>