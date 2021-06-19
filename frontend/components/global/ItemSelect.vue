<template>
    <div id="wrapper" class="w100" :style="wrapperSettings">
        <div class="bar">
            <div class="text-box" @click.stop="openMenu" :style="indexChange">
                <transition name="fade" mode="out-in">
                    <div key="1" class="placeholder" v-if="selectedItems.length==0">
                        <div  style="margin-left: 5px;" :style="{color: color}">{{ placeholder }}</div>
                        <div style="position:relative"><div :class="iconClass"></div></div>
                    </div>
                    <div key="2" class="flex-wrap" v-else>
                        <transition-group class="flex-wrap" name="list" tag="div">
                            <span @click.stop="" class="chip" :style="chipSettings" v-for="(selectedItem, i) in selectedItems" :key="i">{{selectedItem.name}}
                                <span style="margin-left:5px;font-size:15px">
                                    <input type="checkbox" :value="selectedItem" v-model="selectedItems" :id="selectedItem.name"><label class="delete" :for="selectedItem.name">×</label>
                                </span>
                            </span>
                        </transition-group>
                    </div>
                </transition>
            </div>
            <div class="view" @click.stop="">
                <form :class="menuClass" :style="{maxHeight: maxHeight}">
                    <label class="item" v-ripple="ripple" v-for="(item, i) in items" :key="i" :for="item.name"><input type="checkbox" :value="item" v-model="selectedItems" :id="item.name"><label :for="item.name">{{item.name}}</label></label>
                    <label class="item" v-ripple="ripple" @click="menuActive">決定</label>
                    <label class="item" v-ripple="ripple" for="reset"><input type="reset" id="reset" value=""><label for="reset" @click="reset">リセット</label></label>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
interface DataType {isSelect: boolean, menuClass: {'active': boolean,'menu': boolean},iconClass: {'down-icon': boolean,'rotate': boolean}};

export default Vue.extend({
    props:{
        placeholder: String || null,
        width: Number || null,
        height: Number || null,
        color: String || null,
        backgroundColor: String || null,
        ripple: String || null,
        items: Array,
        value: Array,
        maxHeight: String,
        chipColor: String,
        chipTextColor: String,
    },
    data(): DataType {
        return {
            isSelect: false,
            menuClass: {
                'active': false,
                'menu': true
            },
            iconClass:{
                'down-icon': true,
                'rotate': false
            },
        }
    },
    computed:{
        indexChange(){
            const closeStyle = {zIndex: -1, backgroundColor: this.backgroundColor};
            const openStyle = {zIndex: 1,transitionDelay: '.5s', backgroundColor: this.backgroundColor};
            return this.$data.menuClass.active ? closeStyle : openStyle;
        },
        selectedItems: {
            get(){
                return this.value;
            },
            set(value){
                this.$emit("input", value);
            }
        },
        chipSettings(){
            return {backgroundColor: this.chipColor, color: this.chipTextColor}
        },
        wrapperSettings(){
            return {width: `${this.width}px`, margin: 'auto', maxHeight: `${this.maxHeight}`};
        }
    },
    methods:{
        openMenu(){
            if (this.menuClass.active) {
                this.$root.$el.removeEventListener('click', this.menuActive);
            } else {
                this.menuClass.active = true;
                this.iconClass.rotate = true;
                this.$root.$el.addEventListener('click', this.menuActive,{once:true});
            }
        },
        menuActive(){
            this.menuClass.active=false;
        },
        reset(){
            this.selectedItems = [];
            this.menuActive();
        },
        async clear(index: number){
            await this.$store.dispatch('home/clearItem', index);
        }
    }
})
</script>

<style lang="scss" scoped>
#wrapper{
    .bar {
        position:relative;
        min-width:200px;
        .text-box{
            border:solid 1px rgba(0,0,0,.27);
            border-radius:5px;
            padding:5px;
            position:relative;
            z-index:1;
            min-height:34px;
            word-break: break-all;
            cursor: pointer;
            .flex-wrap{
                display: flex;
                flex-wrap: wrap;
            }
            .chip{
                margin:1px 3px;
                padding:1px 9px;
                background-color:rgb(71, 64, 64);
                border-radius:10px;
                font-size:12px;
                pointer-events: none;
                opacity: 1s;
                cursor: initial;
                transition: all .5s;
                .delete{
                    pointer-events: auto;
                    cursor: pointer;
                }
            }
            .chip:hover{
                cursor: none;
                background-color:rgba(32, 26, 26, 0.666);
                transition: all .5s;
                opacity: 0.7;
            }
            .placeholder{
                color:black;
                display:flex;
                justify-content:space-between;
            }
            .down-icon{
                border-radius: 0px 1px 2px 1px;
                position:absolute;
                top:0;
                bottom:0;
                margin:auto;
                right:10px;
                border-right:solid 3px #644a4a;
                border-bottom:solid 3px #644a4a;
                height:12px;
                width:12px;
                transform:rotateZ(45deg) translate(-4px);
                transition: all .5s;
            }
            .rotate{
                transform:rotateZ(-135deg);
                transition: all .3s;
            }
        }
        ::-webkit-scrollbar {
            display: none;
        }
        .chip{
            input[type="checkbox"]{
                display: none;
            }
        }
        .view {
            transform-style:preserve-3d;
            -moz-perspective:100%;
            perspective:100%;
            -o-perspective:100%;
            -ms-perspective:100%;
            position:absolute;
            width: 100%;
            top:0px;
            .menu{
                height:0;
                visibility: hidden;
                opacity: 0;
                width:100%;
                transform: translateY(-25px) rotateX(30deg);
                transition: all .2s;
                transition-delay: .1s;
                transition-timing-function: ease-in;
                border-radius:5px;
                box-shadow: 0 0 0 1px rgb(208, 208, 208);
                overflow-y: scroll;
                label{
                    display: inline-block;
                    width: 100%;
                }
                input[type="checkbox"]{
                    display: none;
                }
                input[type="reset"]{
                    display: none;
                }
                input[type="checkbox"]+label{
                    display: none;
                    cursor: pointer;
                    display: inline-block;
                    position: relative;
                    padding-left: 25px;
                    padding-right: 25px;
                }
                input[type="checkbox"]+label::before{
                    content: "";
                    position: absolute;
                    display: block;
                    box-sizing: border-box;
                    width: 12px;
                    height: 12px;
                    margin: auto;
                    left: 0;
                    top: 0;
                    bottom: 0;
                    border-color:  #585753; /* 枠の色変更 お好きな色を */
                    background-color: #FFF; /* 背景の色変更 お好きな色を */
                    border-radius: 2px;
                    box-shadow: 0 0 1px 1px #3d0076
                }
                input:checked ~ label::before{
                background-color: rgb(0, 55, 253);
                box-shadow: 0 0 1px 1px #004cc5;
                }
                input[type="checkbox"]:checked+label::after{
                    content: "";
                    position: absolute;
                    display: block;
                    box-sizing: border-box;
                    width: 8px;
                    height: 4px;
                    top: 0;
                    bottom: 0;
                    margin: auto;
                    left: 0px;
                    transform: translate(2px,-1px) rotate(-45deg);
                    border-bottom: 2px solid;
                    border-left: 2px solid;
                    border-color:  whitesmoke; /* チェックの色変更 お好きな色を */
                }
                .item{
                    padding: 8px 15px;
                    color: #FAF5EB;
                    cursor: pointer;
                    transition: all .3s;
                    list-style: none;
                    background-color: indigo;
                }
                .item:first-child{
                    border-radius:5px 5px 0 0
                }
                .item:last-child{
                    border-radius:0 0 5px 5px
                }
                .item:hover{
                    background-color: rgb(149, 65, 209);
                    transition: all .3s;
                }
                .item:active{
                    background-color: rgb(102, 0, 175);
                    transition: all .3s;
                }
            }
            .active{
                visibility: visible;
                opacity: 1;
                transform: translateY(0) rotateX(0deg);
                transition: all .2s;
                transition-delay: .1s;
                transition-timing-function: ease-out;
                z-index:3;
                height: 100vh;
            }
        }
    }
}
.w100{
    width:100%;
}
    .list-move{
        transition: transform 1s;
    }
    .list-enter {
        opacity: 0;
    }
    .list-enter-active {
        transition: all 1s;
    }
    .list-leave-active {
        transition: all 1s;
        position:absolute;
    }
    .list-leave-to /* .list-leave-active for below version 2.1.8 */ {
        opacity: 0;
    }
    .fade-enter-active, .fade-leave-active {
        transition: opacity .5s;
    }
    .fade-enter, .fade-leave-to /* .fade-leave-active below version 2.1.8 */ {
        opacity: 0;
    }
</style>