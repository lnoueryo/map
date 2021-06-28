<template>
    <div>
        <nav class="bottom-bar" :style="navStyle">
            <div style="overflow-x:hidden;width:100%;">
                <div class="d-flex" v-if="show">
                    <div class="mx-2" style="width:100%">
                        <v-btn block @click="upWiki" v-if="!position">up</v-btn>
                        <v-btn block @click="downWiki" v-else>down</v-btn>
                    </div>
                    <div class="mx-2" style="width:100%">
                        <v-btn block @click="fade">delete</v-btn>
                    </div>
                </div>
                <div :style="wikiStyle" ref="wiki" v-html="stationInfo"></div>
            </div>
        </nav>
        <div style="position:absolute;bottom:7%;left:50%;transform: translateY(-50%) translateX(-50%);width:100%;padding:0 10px;max-width:300px;z-index:15" v-if="this.$store.getters['home/searching']">
            <v-card color="orange" dark height="40">
                <v-card-text style="height:30px;padding:5px 10px;">
                Please stand by
                <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
                </v-card-text>
            </v-card>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            translateY: 0,
            navStyle: {
                height: 0,
                transform: '',
                transition: 'all .5s'
            },
            wikiStyle: {
                height: 0,
                transition: 'all .5s',
                overflowY: 'hidden',
                overflowX: 'hidden',
            },
            show: false,
            position: false,
        }
    },
    computed:{
        transform(){
            return {transform: `translateY(${this.translateY}px)`, transition: 'all .5s'}
        },
        windowSizeY(){
            return this.$store.getters.windowSize.y;
        },
        stationInfo(){
            return this.$store.getters['home/stationInfo'];
        }
    },
    watch:{
        // windowSizeY:{
        //     handler(value){
        //         this.wikiStyle = Object.assign({},this.wikiStyle, {height: value+'px'});
        //     }
        // },
        stationInfo:{
            handler(){
                this.show = true;
                this.navStyle = Object.assign({},this.navStyle, {height: 100+'px',transform: 'translateY(-100px)'});
                this.wikiStyle = Object.assign({},this.wikiStyle, {height: 40+'px'});
                this.$nextTick(function(){
                    const wiki = this.$refs.wiki;
                    const table = wiki.getElementsByClassName('infobox bordered')[0];
                    table.style.width = ''
                })
            }
        }
    },
    methods:{
        upWiki(){
            this.position = true;
            this.navStyle = Object.assign({},this.navStyle, {height: this.windowSizeY+'px',transform: `translateY(-${this.windowSizeY}px)`});
            this.wikiStyle = Object.assign({},this.wikiStyle, {height: (this.windowSizeY-40)+'px',overflowY: 'scroll'});
        },
        async downWiki(){
            this.position = false;
            const wiki = this.$refs.wiki;
            wiki.scrollTop = 0
            this.navStyle = Object.assign({},this.navStyle, {height: 100+'px',transform: 'translateY(-100px)'});
            this.wikiStyle = Object.assign({},this.wikiStyle, {height: 40+'px',overflowY: 'hidden'});
        },
        fade(){
            this.show = false;
            this.position = false;
            const wiki = this.$refs.wiki;
            wiki.scrollTop = 0
            this.navStyle = Object.assign({},this.navStyle, {height: 0+'px',transform: 'translateY(0px)'});
            this.wikiStyle = Object.assign({},this.wikiStyle, {height: 0+'px',overflowY: 'hidden'});
        }
    }
}
</script>

<style lang="scss" scoped>
    .bottom-bar{
        position:absolute;
        right:0;
        left:0;
        z-index: 10;
        color: black;
        background-color: #ffffff;
    }
    .mw-parser-output{
        position: relative;
        z-index: 10;
        background-color: white;
        margin: auto;
    }
</style>