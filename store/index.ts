import { $axios } from '~/utils/api';

// import { $nuxt } from '~/utils/api'
// import { $nuxt } from 'nuxt'

interface State {
    token: null | string,
    // cropImage: null | string[],
    // message: null | string,
    // listItem: {icons: string[], titles: string[]},
    // btnValidation: {next1: boolean, next2: boolean, send: boolean}
    // croppingBtn: {icons: [{name: string, leftValue: null, rightValue: string, left: boolean, right: boolean}], color: string[]}
  }
  interface Token {
    access: string, refresh: string
  }

const state = {
    token: null,
    // cropImage: [],
    // message: '',
    // btnValidation: {'next1': false, 'next2': true, 'send': true},
    // submitBtn: {'color': 'pink', 'text': true, 'value': '投稿する'},
    // croppingBtn: {icons: [{name: 'mdi-menu-right', leftValue: '', rightValue: 'Next', left: false, right: true}], color: ['primary']},
};

const getters = {

}

const mutations = {
    login(state: State, token: string) {
        state.token = token;
    },
};

const actions = {
    async login (context: any, payload: Token) {
        console.log('success')
        $axios.setToken(payload.access, 'Bearer')
        context.commit('login', payload);
        const stringToken = JSON.stringify(payload)
        localStorage.setItem('token', stringToken)
    },
    isAuth(context: any, payload: string){
        const token = localStorage.getItem('token');
        if (token) {
            const parsedToken = JSON.parse(token)
            context.commit('login', parsedToken);
            $axios.setToken(parsedToken.access, 'Bearer')
            if(payload == 'login'){
                (this as any).$router.push('/')
            }
        }

    }
};

export default {
    state,
    getters,
    mutations,
    actions,
}
// NuxtのVuex内で$routerを使うことになった。
// Nuxtでは

// ```javascript
// $nuxt.$router.push('/')
// ```

// のように使うのだが、storeが現在index.tsのため$nuxtにエラーが発生してしまう。
// なので$axiosと同じ手法で$nuxtを定義した。

// ```typescript:utils/api.ts
// import { NuxtAxiosInstance } from '@nuxtjs/axios';
// import { NuxtApp } from '@nuxt/types/app'
// let $axios: NuxtAxiosInstance;
// let $nuxt: NuxtApp
// export function initializeAxios(axiosInstance: NuxtAxiosInstance): void {
//   $axios = axiosInstance;
// }

// export { $axios, $nuxt };
// ```

// ```store/index.ts
// import { $axios, $nuxt } from '~/utils/api';
// ```

// これでエラーが消えた。
