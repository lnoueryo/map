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
                <v-text-field label="address" v-model="value.address" hint="example of persistent helper text" persistent-hint required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="founded*" v-model="value.founded" required></v-text-field>
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
        address:{
            get(){
                return this.value.company
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {address: value}))
            }
        },
        founded:{
            get(){
                return this.value.line
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {founded: value}))
            }
        },
    }
}
</script>