import { $axios } from '~/utils/api';

interface State {
    token: null | string,
    windowSize: WindowSize
  }
  interface Token {
    access: string, refresh: string
  }
  interface WindowSize {x: number, y: number}

const state = {
    token: null,
    windowSize: {x: 0,y: 0}
};

const getters = {
    
    windowSize(state: any){return state.windowSize}
}

const mutations = {
    login(state: State, token: string) {
        state.token = token;
    },
    windowSize(state: State, payload: WindowSize){
        state.windowSize = Object.assign({}, state.windowSize, payload);
    }
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
    },
    windowSize(context: any, payload: WindowSize){
        context.commit('windowSize', payload)
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
