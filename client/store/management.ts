import { $axios } from '~/utils/api';
interface Company {name: string,created_at: string,updated_at: string}
interface Line {name: string,created_at: string,updated_at: string}
interface Station {name: string,created_at: string,updated_at: string}
type Data = Company[]|Line[]|Station[]
interface State {
    data: string,
    items: Data,
    sortBy: string,
    itemsPerPageArray: number[],
    itemsPerPage: number,
    editIndex: number,
    sortDesc: boolean,
    search: string,
    componentTypes: ['company', 'train-line', 'station'],
}


const state = {
    data: 'company',
    items: [],
    sortBy: 'id',
    itemsPerPageArray: [4, 8, 12, 16, 20, 50, 100],
    itemsPerPage: 50,
    editIndex: -1,
    sortDesc: false,
    search: null,
    componentTypes: ['company', 'train-line', 'station'],
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
        return state.items[state.editIndex];
    },
    filterByKey(state: State, getters: any){
        let copyItems = JSON.parse(JSON.stringify(state.items));
        if (copyItems.length !== 0) {
            const type = getters.checkType(copyItems[0][state.sortBy]);
            let items;
            if (type == 0) {
                items = copyItems.sort((a: Company|Line|Station, b: Company|Line|Station)=>{
                    const condition1 = (a[state.sortBy as never] as string).charCodeAt(0) - (b[state.sortBy as never] as string).charCodeAt(0);
                    const condition2 = (b[state.sortBy as never] as string).charCodeAt(0) - (a[state.sortBy as never] as string).charCodeAt(0);
                    return !state.sortDesc?condition1:condition2;
                })
            } else if(type == 1){
                items = copyItems.sort((a: Company|Line|Station, b: Company|Line|Station)=>{
                    const condition1 = a[state.sortBy as never] as number - b[state.sortBy as never] as number;
                    const condition2 = b[state.sortBy as never] as number - a[state.sortBy as never] as number;
                    return !state.sortDesc?condition1:condition2;
                })
            } else if(type == 2){
                items = copyItems.sort((a: Company|Line|Station, b: Company|Line|Station)=>{
                    const date1 = (new Date(a.created_at)).getTime();
                    const date2 = (new Date(b.created_at)).getTime();
                    const condition1 = date1 - date2;
                    const condition2 = date2 - date1;
                    return !state.sortDesc?condition1:condition2;
                })
            } else {
                items = copyItems.sort((a: Company|Line|Station, b: Company|Line|Station)=>{
                    const date1 = (new Date(a.updated_at)).getTime();
                    const date2 = (new Date(b.updated_at)).getTime();
                    const condition1 = date1 - date2;
                    const condition2 = date2 - date1;
                    return !state.sortDesc?condition1:condition2;
                })
            }
            return items;
        }
        return [];
    },
    checkType: (state: State)=>(data: any)=>{
        if (state.sortBy !== 'created_at'&&state.sortBy !== 'updated_at') {
            if (typeof data === 'string') {
                return 0;
            } else {
                return 1;
            }
        } else {
            if(data == 'created_at'){
                return 2;
            } else {
                return 3;
            }
        }
    },
    filterByWord: (state: State, getters: any)=>{
        return getters.search?getters.filterByKey.filter((item: Company|Line|Station)=>{
            const str = Object.values(item).join("");
            const words = getters.search.trim().replace(/\s+/g,' ');
            const wordArray = words.split(' ');
            console.log(wordArray)
            return wordArray.length==1?str.includes(words):wordArray.every((word: string)=>{return str.includes(word)});
        }):getters.filterByKey;
    },
    search(state: State){
        return state.search;
    },
    itemsPerPage(state: State){
        return state.itemsPerPage;
    },
    itemsPerPageArray(state: State){
        return state.itemsPerPageArray;
    },
    editIndex(state: State){
        return state.editIndex;
    },
    editDialog(state: State){
        return state.editIndex !==-1;
    },
    component(state: State, getters: any){
        return state.componentTypes[getters.changeList];
    }
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
    },
    items(state: State, payload: Data){
        state.items = payload;
    },
    sortDesc(state: State, payload: any){
        state.sortDesc = payload;
    },
    search(state: State, payload: string){
        state.search = payload;
    },
    itemsPerPage(state: State, payload: number){
        state.itemsPerPage = payload;
    }
};

const actions = {
    async items(context: any, payload: string){
        const response = await $axios.$get(`/api/management/${payload}/`);
        context.commit('items', response)
    },
    data(context: any, payload: string){
        context.commit('data', payload)
    },
    sortBy(context: any, payload: string){
        context.commit('sortBy', payload)
    },
    editIndex(context: any, payload: number){
        context.commit('editIndex', payload)
    },
    sortDesc(context: any, payload: any){
        context.commit('sortDesc', payload)
    },
    search(context: any, payload: string){
        context.commit('search', payload)
    },
    itemsPerPage(context: any, payload: number){
        context.commit('itemsPerPage', payload)
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
