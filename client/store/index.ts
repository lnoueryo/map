import { $axios } from '~/utils/api';

interface State {
    token: null | string,
    windowSize: WindowSize,
    map: any,
    errorDialog: boolean
}
interface Token {
    access: string, refresh: string
}
interface WindowSize { x: number, y: number };

const state = {
    token: null,
    windowSize: { x: 0, y: 0 },
    errorDialog: false
};

const getters = {
    windowSize: (state: State) => state.windowSize,
    errorDialog: (state: State) => state.errorDialog
}

const mutations = {
    login(state: State, token: string) {
        state.token = token;
    },
    windowSize(state: State, payload: WindowSize) {
        state.windowSize = Object.assign({}, state.windowSize, payload);
    },
    errorDialog(state: State, payload: boolean) {
        state.errorDialog = payload;
    },
};

const actions = {
    async login(context: any, payload: Token) {
        console.log('success')
        $axios.setToken(payload.access, 'Bearer')
        context.commit('login', payload);
        const stringToken = JSON.stringify(payload)
        localStorage.setItem('token', stringToken)
    },
    isAuth(context: any, payload: string) {
        const token = localStorage.getItem('token');
        if (token) {
            const parsedToken = JSON.parse(token)
            context.commit('login', parsedToken);
            $axios.setToken(parsedToken.access, 'Bearer')
            if (payload == 'login') {
                (this as any).$router.push('/')
            }
        }
    },
    windowSize(context: any, payload: WindowSize) {
        context.commit('windowSize', payload)
    },
    errorDialog: (context: any, payload: boolean) => {
        context.commit('errorDialog', payload)
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
