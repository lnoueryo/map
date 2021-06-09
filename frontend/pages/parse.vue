<template>
    <div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="text" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json2" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json" style="background-color:white;width:100%;"></textarea></div>
    </div>
</template>

<script>
export default {
    data(){
        return {
            text: 'null'
        }
    },
    computed:{
        json(){
            return this.text.replace(/\'/g, '"').replace(/\s/g, '').replace(/({"city")(.+?)(]]})/g, '$1$2$3,')
        },
        json2(){
            return this.text.replace(/nan/g, '')
        },
    }
}
</script>