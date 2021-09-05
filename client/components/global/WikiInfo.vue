<template>
    <div>
        <div ref="wiki" class="wiki">
            <div v-html="wikiData" v-if="wikiData"></div>
            <div v-else class="centering">
                <div>マーカーをクリックして駅情報を取得しましょう</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    props: ['wikiData'],
    watch: {
        wikiData: {
            handler() {
                this.$nextTick(() => {
                    const wiki = this.$refs.wiki as HTMLDivElement;
                    wiki.scrollTop = 0
                    const table = wiki.getElementsByClassName('infobox bordered')[0] as HTMLDivElement;
                    if (table) {
                        table.style.width = ''
                        table.style.margin = 'auto'
                    }
                })
            }
        }
    }
})
</script>

<style lang="scss" scoped>
    .wiki {
        height: 100vh;
        background-color: white;
        color: black;
        // overflow-x: hidden;
        // overflow-y: scroll;
        max-height: calc(100vh - 70px);
    }
    .centering {
        display: flex;
        align-items: center;
        height: 100%;
    }
</style>