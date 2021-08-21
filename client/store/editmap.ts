import { $axios } from '~/utils/api';
interface Line {id: number, company_id: number, name: string, polygon: Polygon, color: string,stations: Station[]};
interface Station {name: string,id:number,line_id:number,order:number,prefecture:string,lat:number,lng:number,company_id:number,city_code: string}
interface Polygon {lat: number, lng: number}[]
interface State {
    lineStation: Line
  }
interface Token {
    access: string, refresh: string
}
interface WindowSize {x: number, y: number};

const state = {
    lineStation: []
};

const getters = {
    lineStation: (state: State) =>{return state.lineStation},
}

const mutations = {
    lineStation(state: State, payload: Line) {
        state.lineStation = payload;
        console.log(state.lineStation)
    },
};

const actions = {
    async getLineStation(context: any, payload: WindowSize){
        const response = await $axios.$get('/api/management/line/station/');
        context.commit('lineStation', response)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
