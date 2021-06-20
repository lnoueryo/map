<template>
    <div>
        <v-row>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="id" :value="value.id" required disabled></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="name" v-model="value.name" hint="example of helper text only on focus"></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="company" v-model="value.company" hint="example of persistent helper text" persistent-hint required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="line*" v-model="value.line" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="lat*" v-model="value.lat" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="lng*" v-model="value.lng" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="12" md="12">
                <v-text-field label="prefecture*" v-model="value.prefecture" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
                <v-select :items="['0-17', '18-29', '30-54', '54+']" label="Age*" required></v-select>
            </v-col>
            <v-col cols="12" sm="6">
                <v-autocomplete :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']" label="Interests" multiple></v-autocomplete>
            </v-col>
        </v-row>
    </div>
</template>

<script>
export default {
    props: ['value'],
    computed:{
        name:{
            get(){
                return this.value.name
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {name: value}))
            }
        },
        company:{
            get(){
                return this.value.company
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {company: value}))
            }
        },
        line:{
            get(){
                return this.value.line
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {line: value}))
            }
        },
        prefecture:{
            get(){
                return this.value.prefecture
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {prefecture: value}))
            }
        },
        lat:{
            get(){
                return this.value.lat
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {lat: value}))
            }
        },
        lng:{
            get(){
                return this.value.lng
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {lng: value}))
            }
        },
    }
}
</script>