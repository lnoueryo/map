<template>
    <div class="w100" :style="{width: `${width}px`}">
        <div class="bar">
            <div class="text-box" @click.stop="openMenu" :style="indexChange">
                <div class="placeholder" v-if="selectedItems.length==0">
                    <div style="margin-left: 5px;" :style="{color: color}">{{ placeholder }}</div>
                    <div style="position:relative"><div :class="iconClass"></div></div>
                </div>
                <span v-else><span class="chip" v-for="(selectedItem, i) in selectedItems" :key="i">{{selectedItem}}<span style="margin-left:5px;font-size:15px" @click.stop="clear(i)">×</span></span></span>
            </div>
            <div class="view" @click.stop="">
                <form :class="menuClass">
                    <label class="item" v-ripple="ripple" v-for="(item, i) in items" :key="i" :for="item"><input type="checkbox" :value="item" v-model="selectedItems" :id="item"><label :for="item">{{item.text}}</label></label>
                    <label class="item" v-ripple="ripple" @click="openMenu">決定</label>
                    <label class="item" v-ripple="ripple" for="reset"><input type="reset" id="reset" value=""><label for="reset" @click="reset">リセット</label></label>
                </form>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    props:{
        placeholder: String || null,
        width: Number || null,
        color: String || null,
        backgroundColor: String || null,
        ripple: Boolean || null
    },
    data() {
        return {
            items: [
                {name: 'JR', text:'JR'},
                {name: 'Keio', text:'京王電鉄'},
                {name: 'Toei', text:'都営地下鉄'},
                {name: 'TokyoMetro', text:'東京メトロ'},
                {name: 'Seibu', text:'西武鉄道'},
                {name: 'Tobu', text:'東武鉄道'},
                {name: 'OdakyuDentetsu', text:'小田急電鉄'},
            ],
            // items: ['JR', '京王電鉄', '都営地下鉄', '東京メトロ'],
            value: '',
            isSelect: false,
            menuClass: {
                'active': false,
                'menu': true
            },
            iconClass:{
                'down-icon': true,
                'rotate': false
            },
            selectedItems: []
        }
    },
    computed:{
        indexChange(){
            return (this as any).menuClass.active ? {zIndex: 0, backgroundColor: this.backgroundColor} : {zIndex: 1,transitionDelay: '.5s', backgroundColor: this.backgroundColor};
        }
    },
    methods:{
        openMenu(){
            const that = this;
            if (this.menuClass.active) {
                this.$root.$el.removeEventListener('click',that.menuActive);
                this.menuActive();
            } else {
                this.menuClass.active = true;
                this.iconClass.rotate = true;
                this.$root.$el.addEventListener('click',that.menuActive,{once:true});
            }
        },
        menuActive(){
            this.menuClass.active=false;
            this.iconClass.rotate=false;
        },
        reset(){
            this.selectedItems.length = 0;
            this.menuActive();
        },
        clear(index: number){
            this.selectedItems.splice(index,1)
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
        .chip{
            margin:0 3px;
            padding:3px 9px;
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
                padding: 9px 15px;
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
            z-index:1;
        }
    }
}
.w100{
    width:100%;
}
</style>