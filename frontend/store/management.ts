import { $axios } from '~/utils/api';
interface Company {name: string}
interface Line {name: string}
interface Station {name: string}
type Data = Company[]|Line[]|Station[]
interface State {
    data: string,
    items: Data,
    sortBy: string,
    editIndex: number,
    selectedItem: Company|Line|Station
}


const state = {
    data: 'station',
    items: [],
    sortBy: 'id',
    editIndex: -1,
    selectedItem: null,
};

const getters = {
    data(state: State){
        return state.data;
    },
    changeList(state: State){
        const data = ['company', 'line', 'station'];
        const index = data.findIndex((v)=>{
            return v == state.data;
        })
        return index;
    },
    sortKeys(state: State){
        if (state.items.length !== 0)return Object.keys(state.items[0]);
        return;
    },
    items(state: State){
        return state.items;
    },
    sortBy(state: State){
        return state.sortBy
    },
    selectedItem(state: State){
        return state.selectedItem;
    },
}

const mutations = {
    data(state: State, payload: string){
        state.data = payload;
    },
    sortBy(state: State, payload: string){
        state.sortBy = payload;
    },
    editIndex(state: State, payload: number){
        state.editIndex = payload;
        state.selectedItem = state.items[payload];
    },
    selectedItem(state: State, payload: Station){
        state.selectedItem = payload;
    },
    items(state: State, payload: Data){
        state.items = payload;
    },
};

const actions = {
    data(context: any, payload: string){
        context.commit('data', payload)
    },
    sortBy(context: any, payload: string){
        context.commit('sortBy', payload)
    },
    editIndex(context: any, payload: number){
        context.commit('editIndex', payload)
    },
    selectedItem(context: any, payload: string){
        context.commit('selectedItem', payload)
    },
    async items(context: any, payload: string){
        const response = await $axios.$get(`/api/management/${payload}/`);
        context.commit('items', response)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
