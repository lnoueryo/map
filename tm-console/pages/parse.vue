<template>
    <div>
        <textarea>{{stations}}</textarea>
        <textarea v-model="text"></textarea>
        <textarea v-model="removeSpace"></textarea>
        <!-- <textarea v-if="stations.length!==0" v-html="remove(stations)"></textarea> -->
        <!-- <textarea name="" id="" cols="30" rows="10">{{stations}}</textarea> -->
        <!-- <v-btn @click="index-=1">back</v-btn>
        <v-btn @click="index+=1">next</v-btn>
        {{deleteLines[index]}}
        <v-btn @click="index-=1">back</v-btn>
        <v-btn @click="index+=1">next</v-btn>
        <textarea v-if="deleteLines[index]" v-model="deleteLines[index].polygon"></textarea> -->
        <!-- {{deleteLines[index].polygon}} -->
        <!-- <div v-for="(line,i) in deleteLines" :key="i">{{line}}</div> -->
        <!-- {{deleteLines}} -->
        <!-- <div><textarea name="" id="" cols="30" rows="20" v-model="text" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json4" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json2" style="background-color:white;width:100%;"></textarea></div>
        <div><textarea name="" id="" cols="30" rows="20" v-model="json3" style="background-color:white;width:100%;"></textarea></div> -->
    </div>
</template>

<script>
export default {
    data(){
        return {
            text: 'null',
            lines: [],
            index: 72,
            stations: []
        }
    },
    computed:{
        // deleteLines(){
        //     var arr = []
        //     var a = this.lines.forEach(line =>{ delete line.stations;arr.push(line)});
        //     var foundValue = arr.find((a)=>{
        //         return a.id === 1
        //     })
        //     arr = arr.sort((a,b)=>{return a.id - b.id})
        //     return arr;
        // },
        removeSpace(){
            return this.text.replace(/\s/g, '');
        },
        // json(){
        //     return this.text.replace(/\'/g, '"').replace(/\s/g, '').replace(/({"city")(.+?)(]]})/g, '$1$2$3,')
        // },
        // json2(){
        //     return this.text.replace(/({)(.+?)(})/g, '\'$1$2$3\'')
        // },
        // json3(){
        //     return this.text.replace(/\'/g, '')
        // },
        // json4(){
        //     return this.text.replace(/\\|\'|^("{)(.+?)(}")/g, '').replace(/\"{/g,'{').replace(/\}"/g,'}')
        // },
    },
    async created(){
        // const response = await this.$axios.$get('/api/map/station/polygon/');
        // this.lines = response;
        // const response2 = await this.$axios.$get('/api/map/');
        const response = await this.$axios.$get(`/api/management/station/`);
        this.stations = response;
    },
    methods:{
        remove(a){
            return a.replace(/\s/g, '');
        },
    }
}
</script>
