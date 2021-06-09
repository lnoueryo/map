<template>
    <div>
        <v-form>
            <v-text-field name="name" label="label" id="id" v-model="loginRequired.email"></v-text-field>
            <v-text-field name="name" label="label" id="id" v-model="loginRequired.password"></v-text-field>
        </v-form>
        <div>{{users}}</div>
        <v-btn color="success" @click="login">login</v-btn>
        <v-btn color="success" @click="get">get</v-btn>
    </div>
</template>
<script lang="ts">
import Vue, { PropOptions } from 'vue'

interface User {
    firstName: string
    lastName: string
}

export default Vue.extend({

// props: {
//   user: {
//     type: Object,
//     required: true
//   } as PropOptions<User>
// },

data () {
    return {
        message: 'This is a message',
        loginRequired: {email: null, password: null},
        users: null
    }
},
// computed: {
//   fullName (): string {
//     return `${this.user.firstName} ${this.user.lastName}`
//   }
// },
methods: {
    async login(){
        const response = await this.$axios.$post('/api/token/', this.loginRequired);
        this.$store.dispatch('login', response)
    },
    async get(){
        const response = await this.$axios.$get('/api/users/');
        this.users = response
        console.log(response)
    },
}
})
</script>