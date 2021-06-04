import { $axios } from '~/utils/api';
interface State {
    lines: Line[],
    selectedItems: {name: string, text: string}[],
    map: any,
    currentBounds: Bounds,
    markerSwitch: boolean,
    lineSwitch: boolean,
  }
interface Line {id: number, company_name: string, line_name: string, polygon: Polygon, color: string};
interface Polygon {lat: number, lng: number}[]
interface MapOptions {center: google.maps.LatLng, restriction: {latLngBounds: Bounds, strictBounds: boolean} | null, zoom: number};
interface Bounds {north: number, south: number, west: number, east: number};
const state = {
    lines: [],
    selectedItems: [],
    map: null,
    currentBounds: {south: 0, north: 0,east: 0, west: 0},
    markerSwitch: false,
    lineSwitch: false
};

const getters = {
    lines:(state: State)=>{
        const items: string[] = [];
        state.selectedItems.forEach((item)=>{
            items.push(item.name);
        })
        let selectedLines;
        if (state.selectedItems.length!==0) {
            selectedLines = state.lines.filter((line)=>{
                return items.includes(line.company_name);
            });
        } else {
            selectedLines = state.lines;
        }
        return selectedLines;
    },
    selectedItems: (state: State) => {return state.selectedItems;},
    bounds: (state: State) =>{return state.currentBounds;},
    markerSwitch: (state: State) =>{return state.markerSwitch;},
    lineSwitch: (state: State) =>{return state.lineSwitch;},
}

const mutations = {
    setLines(state: State, payload: Line[]){
        payload.forEach(line => {
            state.lines.push(line);
        });
    },
    selectedItems(state: State, payload: {name: string, text: string}[]){
        state.selectedItems = payload;
    },
    clearItem(state: State, payload: number){
        state.selectedItems.splice(payload,1);
    },
    map(state: State, payload: any){
        console.log(payload)
        state.map = payload
    },
    currentBounds(state: State, payload: Bounds){
        state.currentBounds = Object.assign({},state.currentBounds,payload)
    },
    markerSwitch(state: State, payload: boolean){
        state.markerSwitch = payload;
    },
    lineSwitch(state: State, payload: boolean){
        state.lineSwitch = payload;
    },
};

const actions = {
    async getLines(context: any){
        const response = await $axios.$get('/api/map/station/polygon/');
        context.commit('setLines', response);
    },
    resetPolyline(context: any, payload: google.maps.Polyline[]){
        payload.forEach(polyline => {
            polyline.setMap(null);
        });
    },
    resetMarkers(_: any, payload: google.maps.Marker[][]){
        payload.forEach((markers)=>{
            markers.forEach((marker)=>{
                marker.setMap(null);
            })
        })
    },
    selectedItems(context: any, payload: {name: string, text: string}[]){
        context.commit('selectedItems', payload)
    },
    clearItem(context: any, payload: number){
        context.commit('clearItem', payload);
    },
    getCurrentBounds(context: any, payload: Bounds){
        context.commit('currentBounds', payload)
    },
    changeMarkerSwitch(context: any, payload: boolean){
        context.commit('markerSwitch',payload)
    },
    changeLineSwitch(context: any, payload: boolean){
        context.commit('lineSwitch',payload)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
