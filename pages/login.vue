<template>
    <div>
        <v-form>
            <v-text-field name="name" label="label" id="id" v-model="loginRequired.email"></v-text-field>
            <v-text-field name="name" label="label" id="id" v-model="loginRequired.password"></v-text-field>
        </v-form>
        <div>{{error}}</div>
        <v-btn color="success" @click="login">login</v-btn>
    </div>
</template>
<script lang="ts">
import Vue from 'vue'

interface User {
    firstName: string
    lastName: string
}

export default Vue.extend({

data () {
    return {
        loginRequired: {email: 'a@co.jp', password: 'a'},
        // loginRequired: {email: null, password: null},
        users: null,
        error: ''
    }
},

methods: {
    async login(){
        try {
            const response = await this.$axios.$post('/api/token/', this.loginRequired);
            this.$store.dispatch('login', response)
            this.$router.push('/')
        } catch (error) {
            if (error.response.status == 401) {
                this.error = 'パスワードが違います'
            }
            if (error.response.status == 429) {
                this.error = '回数が上限を超えました。1分後に再度お試しください'
            }
        }
    },
    async get(){
        const response = await this.$axios.$get('/api/users/');
        this.users = response
        console.log(response)
    },
}
})
</script>