<template>
    <div class="w100" style="max-height: calc(100vh - 500px)" :style="{width: `${width}px`, margin: 'auto'}">        <div class="bar">
            <div class="text-box" @click.stop="openMenu" :style="indexChange">
                <div class="placeholder" v-if="selectedItems.length==0">
                    <div style="margin-left: 5px;" :style="{color: color}">{{ placeholder }}</div>
                    <div style="position:relative"><div :class="iconClass"></div></div>
                </div>
                <div class="flex-wrap" v-else>
                    <span class="chip" v-for="(selectedItem, i) in selectedItems" :key="i">{{selectedItem.name}}
                        <span style="margin-left:5px;font-size:15px">
                            <input type="checkbox" :value="selectedItem" v-model="selectedItems" :id="selectedItem.name"><label :for="selectedItem.name">×</label>
                        </span>
                    </span>
                    <!-- <span class="chip" v-for="(selectedItem, i) in selectedItems" :key="i">{{selectedItem.name}}<span style="margin-left:5px;font-size:15px" @click.stop="clear(i)">×</span></span> -->
                </div>
            </div>
            <div class="view" @click.stop="">
                <form :class="menuClass">
                    <label class="item" v-ripple="ripple" v-for="(item, i) in items" :key="i" :for="item.name"><input type="checkbox" :value="item" v-model="selectedItems" :id="item.name"><label :for="item.name">{{item.name}}</label></label>
                    <label class="item" v-ripple="ripple" @click="openMenu">決定</label>
                    <label class="item" v-ripple="ripple" for="reset"><input type="reset" id="reset" value=""><label for="reset" @click="reset">リセット</label></label>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue';
export default Vue.extend({
    props:{
        placeholder: String || null,
        width: Number || null,
        height: Number || null,
        color: String || null,
        backgroundColor: String || null,
        ripple: String || null,
        items: Array,
        value: Array
    },
    data() {
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
            return (this as any).menuClass.active ? {zIndex: -1, backgroundColor: this.backgroundColor} : {zIndex: 1,transitionDelay: '.5s', backgroundColor: this.backgroundColor};
        },
        selectedItems: {
            get(){
                return this.value;
            },
            set(value){
                this.$emit("input", value);
            }
        }
        // selectedItems: {
        //     get(){
        //         return this.$store.getters['home/selectedItems']
        //     },
        //     set(value){
        //         this.$store.dispatch('home/selectedItems', value)
        //     }
        // }
    },
    methods:{
        openMenu(){
            const that = this;
            if ((this as any).menuClass.active) {
                this.$root.$el.removeEventListener('click',(that as any).menuActive);
                (this as any).menuActive();
            } else {
                (this as any).menuClass.active = true;
                (this as any).iconClass.rotate = true;
                this.$root.$el.addEventListener('click',(that as any).menuActive,{once:true});
            }
        },
        menuActive(){
            (this as any).menuClass.active=false;
        },
        reset(){
            (this as any).selectedItems = [];
            (this as any).menuActive();
        },
        async clear(index: number){
            await this.$store.dispatch('home/clearItem', index);
        }
    }
})
</script>

<style lang="scss" scoped>
.bar {
    position:relative;
    min-width:200px;
    .text-box{
        border:solid 1px rgba(0,0,0,.27);
        border-radius:5px;
        padding:5px;
        position:relative;
        z-index:1;
        cursor: pointer;
        min-height:34px;
        word-break: break-all;
        .flex-wrap{
            display: flex;
            flex-wrap: wrap;
        }
        .chip{
            margin:1px 3px;
            padding:1px 9px;
            background-color:black;
            border-radius:10px;
            font-size:12px
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
            max-height: calc(100vh - 70px);
            overflow-y: scroll;
        }
    }
}
.w100{
    width:100%;
}
</style>