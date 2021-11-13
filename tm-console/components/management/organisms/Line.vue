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
                <v-text-field label="color*" v-model="value.color" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="line_code*" v-model="value.line_code" required></v-text-field>
            </v-col>
            <v-col cols="12" sm="6" md="6">
                <v-text-field label="company_id*" v-model="value.company_id" required></v-text-field>
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
        color:{
            get(){
                return this.value.color
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {color: value}))
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
        line_code:{
            get(){
                return this.value.line_code
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {line_code: value}))
            }
        },
        company_id:{
            get(){
                return this.value.company_id
            },
            set(value){
                this.$emit('input', Object.assign({}, this.value, {company_id: value}))
            }
        },
    }
}
</script>