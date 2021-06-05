import { $axios } from '~/utils/api';
interface State {
    lines: Line[],
    selectedItems: {name: string, text: string}[],
    map: any,
    currentBounds: Bounds,
    markerSwitch: boolean,
    lineSwitch: boolean,
    selectedMarker: Station,
    searchWord: string,
    stationInfo: null|string,
  }
interface Line {id: number, company_name: string, line_name: string, polygon: Polygon, color: string,stations: Station[]};
interface Polygon {lat: number, lng: number}[]
interface Bounds {north: number, south: number, west: number, east: number};
interface Station {company_name: string,id:number,line_name:string,order:number,pref_name:string,station_lat:number,station_lon:number,station_name:string}

const state = {
    lines: [],
    selectedItems: [],
    map: null,
    currentBounds: {south: 0, north: 0,east: 0, west: 0},
    markerSwitch: false,
    lineSwitch: false,
    selectedMarker: {},
    searchWord: null,
    stationInfo: null,
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
    selectedMarker: (state: State) =>{return state.selectedMarker;},
    showNumberOfMarkers: (state: State, getters: any) =>{
        return getters.lines.reduce(function(sum:any, line:any){
            return sum + (getters.boundsFilter(line.stations)).length;
        }, 0);
    },
    boundsFilter: (state:State) =>(stations: Station[]) =>{
        const filteredStations = stations.filter((station)=>{
            const verticalCondition = state.currentBounds.west < station.station_lon && state.currentBounds.east > station.station_lon;
            const horizontalCondition = state.currentBounds.south < station.station_lat && state.currentBounds.north > station.station_lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
    },
    searchStations: (state: State, getters: any) =>{
        const stations: Station[] = [];
        getters.lines.forEach((line: Line) => {
            line.stations.forEach(station => {
                if (station.station_name.indexOf(state.searchWord) > -1) {
                    stations.push(station)
                }
            });
        });
        return state.searchWord?getters.removeOverlap(stations):[];
    },
    removeOverlap: (state:State) =>(stations: Station[]) =>{
        let map = new Map(stations.map(station => [station.station_name, station]));
        return Array.from(map.values());
    },
    stationInfo(state: State){return state.stationInfo},
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
    selectMarker(state: State, payload: Station){
        state.selectedMarker = Object.assign({},state.selectedMarker,payload);
    },
    searchWord(state: State, payload: string){
        state.searchWord = payload;
    },
    stationInfo(state: State, payload: string){
        state.stationInfo = payload;
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
    selectMarker(context: any, payload: Station){
        context.commit('selectMarker',payload)
    },
    searchWord(context: any, payload: string){
        context.commit('searchWord',payload)
    },
    async getStationInfo(context: any, payload: string){
        const response = await $axios.$post('/api/map/station/line/wiki/',payload);
        context.commit('stationInfo', response)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
