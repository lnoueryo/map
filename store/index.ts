import { $axios } from '~/utils/api';

interface State {
    token: null | string,
    windowSize: WindowSize,
    lines: Line[],
    map: google.maps.Map | null
  }
interface Token {
    access: string, refresh: string
}
interface WindowSize {x: number, y: number};
interface Line {id: number, company_name: string, line_name: string, polygon: Polygon, color: string};
interface Polygon {lat: number, lng: number}[]
interface MapOptions {center: google.maps.LatLng, restriction: {latLngBounds: Bounds, strictBounds: boolean} | null, zoom: number};
interface Bounds {north: number, south: number, west: number, east: number};
const state = {
    token: null,
    windowSize: {x: 0,y: 0},
    lines: [],
    map: null
};

const getters = {
    windowSize(state: any){return state.windowSize},
    lines(state: any){return state.lines},
}

const mutations = {
    login(state: State, token: string) {
        state.token = token;
    },
    windowSize(state: State, payload: WindowSize){
        state.windowSize = Object.assign({}, state.windowSize, payload);
    },
    setLines(state: State, payload: Line[]){
        payload.forEach(line => {
            state.lines.push(line)
        });
    },
    setMap(state: State, payload: google.maps.Map){
        state.map = payload;
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
    },
    async getLines(context: any){
        const response = await $axios.$get('/api/map/station/polygon/');
        context.commit('setLines', response);
    },
    resetPolyline(context: any, payload: google.maps.Polyline[]){
        payload.forEach(polyline => {
            polyline.setMap(null);
        });
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
