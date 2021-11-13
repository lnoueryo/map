import { $axios } from '~/utils/api';
import VueRouter from "vue-router";
interface State {
    user: User
    windowSize: WindowSize,
    errorDialog: boolean,
    tables: Table[]
}
interface User {
    id: number, name: string, email: string, password: string
}
interface Table {
    name: string, columns: string[]
}
interface WindowSize { x: number, y: number };

const state = {
    user: {
        id: '',
        name: '',
        email: ''
    },
    windowSize: { x: 0, y: 0 },
    errorDialog: false,
    tables: []
};

const getters = {
    windowSize: (state: State) => state.windowSize,
    errorDialog: (state: State) => state.errorDialog,
    tables: (state: State) => state.tables,
}

const mutations = {
    user(state: State, payload: User) {
        state.user = payload;
    },
    windowSize(state: State, payload: WindowSize) {
        state.windowSize = Object.assign({}, state.windowSize, payload);
    },
    errorDialog(state: State, payload: boolean) {
        state.errorDialog = payload;
    },
    tables: (state: State, payload: Table[]) => {
        state.tables = payload;
    }
};

const actions = {
    async login(context: any, payload: User) {
        let status: {status: boolean, message: string};
        try {
            const response = await $axios.post('/api/user/login/', payload);
            context.commit('user', response.data);
            status = {status: true, message: ''};
        } catch (err: any) {
            if (err.response.status == 401) {
                const message = 'パスワードまたはEmailアドレスが間違っているようです';
                status = {status: false, message: message};
            } else if (err.response.status == 429) {
                const message = '回数が上限を超えました。1分後に再度お試しください';
                status = {status: false, message: message};
            } else {
                status = {status: false, message: '不明'};
            }
        }
        return status;
    },
    logout: async(context: any) => {
        let status = {status: false};
        try {
            const response = await $axios.get('/api/user/logout/');
            context.commit('user', response);
            status = {status: true};
        } catch(err: any) {
            console.log(err)
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
            else context.dispatch('errorDialog', true);
        }
        return status;
    },
    isLogin: async (context: any, payload: string) => {
        const response = await $axios.get('/api/user/auth/');
        console.log(response)
    },
    windowSize(context: any, payload: WindowSize) {
        context.commit('windowSize', payload)
    },
    errorDialog: (context: any, payload: boolean) => {
        context.commit('errorDialog', payload)
    },
    getTables: async(context: any) => {
        try {
            const response = await $axios.get('/api/map/table/');
            context.commit('tables', response.data);
        } catch(err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
            else context.dispatch('errorDialog', true);
        }
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
