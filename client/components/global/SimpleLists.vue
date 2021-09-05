<template>
    <div>
        <div class="title"><slot></slot></div>
        <transition-group name="list" tag="div">
            <div v-for="(item, i) in $store.getters['home/boundsFilter'](items)" :key="i" style="position:relative">
                <div>
                    <div class="item" style="width:100%;color:black" @click="onClickList(item)">
                        <div>{{item.name}}</div>
                    </div>
                </div>
            </div>
        </transition-group>
    </div>
</template>

<script>
export default {
    props: ['items'],
    methods: {
        onClickList(item) {
            this.$emit('item', item)
        }
    },
}
</script>

<style lang="scss" scoped>
    .title {
        text-align: center;
        border-radius: 5px;
        color: white;
        background-color: #452929;
        width: 100%;
        display: block;
        padding: 10px;
        transition: all .5s;
        cursor: pointer;
    }
    .title:hover {
        opacity: .7;
        transition: all .5s;
    }
    .title:active {
        opacity: .9;
        transition: all .5s;
    }
    .name {
        text-align: center;
        border-radius: 5px;
        color: black;
        width: 100%;
        display: block;
        padding: 10px;
        transition: all .5s;
        cursor: pointer;
        background-color: white;
    }
    .name:hover {
        opacity: .7;
        transition: all .5s
    }
    .name:active {
        opacity: .9;
    }
    .list-move {
        transition: transform 1s;
    }
    .list-enter {
        opacity: 0;
        transform: translateX(256px);
    }
    .list-enter-active {
        transition: all 1s;
    }
    .list-leave-active {
        transition: all 1s;
        position: absolute;
    }
    .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
        opacity: 0;
        transform: translateX(256px);
    }
    .item {
        padding: 10px;
        background-color: white;
        width: 100%;
        transition: all .5s;
        cursor: pointer;
        text-align: center;
    }
    .item:hover {
        opacity: 0.7;
        transition: all .5s;
    }
    .item:active {
        opacity: 0.9;
        transition: all .5s;
    }
</style>