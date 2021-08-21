import { $axios } from '~/utils/api';

interface State {
    token: null | string,
    windowSize: WindowSize,
    map: any
  }
interface Token {
    access: string, refresh: string
}
interface WindowSize {x: number, y: number};

const state = {
    token: null,
    windowSize: {x: 0,y: 0},
};

const getters = {
    windowSize: (state: State)=>state.windowSize,
}

const mutations = {
    login(state: State, token: string) {
        state.token = token;
    },
    windowSize(state: State, payload: WindowSize){
        state.windowSize = Object.assign({}, state.windowSize, payload);
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
    },
    windowSize(context: any, payload: WindowSize){
        context.commit('windowSize', payload)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
