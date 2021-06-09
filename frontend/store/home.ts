import { $axios } from '~/utils/api';
import companies from '~/assets/json/company.json'
interface State {
        companies: Company[]
        selectedCompanyItems: Company[],
        selectedLineItems: Line[],
        map: any,
        currentBounds: Bounds,
        markerSwitch: boolean,
        lineSwitch: boolean,
        selectedMarker: Station,
        searchWord: string,
        stationInfo: null|string,
    }
interface Polygon {lat: number, lng: number}[]
interface Bounds {north: number, south: number, west: number, east: number};
interface Company {id: number, name: string, address: string, founded: string, lines: Line[]};
interface Line {id: number, company_id: number, name: string, polygon: Polygon, color: string,stations: Station[]};
interface Station {name: string,id:number,line_id:number,order:number,prefecture:string,lat:number,lng:number,company_id:number}

const state = {
    companies: [],
    selectedCompanyItems: [],
    selectedLineItems: [],
    map: null,
    currentBounds: {south: 0, north: 0,east: 0, west: 0},
    markerSwitch: false,
    lineSwitch: false,
    selectedMarker: {},
    searchWord: null,
    stationInfo: null,
};

const getters = {
    companies:(state: State)=>{return companies;},
    lineItems:(state: State, getters: any)=>{
        const lines: Line[] = [];
        getters.companies.forEach((company: Company)=>{
            company.lines.forEach(line => {
                lines.push(line);
            });
        })
        return getters.companyFilter(lines);
    },
    lines:(state: State, getters: any)=>{
        const lines: Line[] = [];
        getters.companies.forEach((company: Company)=>{
            company.lines.forEach(line => {
                lines.push(line);
            });
        })
        return getters.filteredLines(lines);
    },
    filteredLines:(state: State, getters: any)=>(lines: Line[]) =>{
        let filteredLines = getters.companyFilter(lines);
        filteredLines = getters.lineFilter(filteredLines);
        return filteredLines;
    },
    companyFilter: (state: State) => (lines: Line[]) => {
        const companyIds: number[] = [];
        state.selectedCompanyItems.forEach((item)=>{
            companyIds.push(item.id);
        })
        let selectedLines;
        if (state.selectedCompanyItems.length!==0) {
            selectedLines = lines.filter((line)=>{
                return companyIds.includes(line.company_id);
            });
        } else {
            selectedLines = lines;
        }
        return selectedLines;
    },
    lineFilter: (state: State) => (lines: Line[], items: number[]) => {
        const lineIds: number[] = [];
        state.selectedLineItems.forEach((item)=>{
            lineIds.push(item.id);
        })
        let selectedLines;
        if (state.selectedLineItems.length!==0) {
            selectedLines = lines.filter((line)=>{
                return lineIds.includes(line.id);
            });
        } else {
            selectedLines = lines;
        }
        return selectedLines;
    },
    selectedCompanyItems: (state: State) => {return state.selectedCompanyItems;},
    selectedLineItems: (state: State) => {return state.selectedLineItems;},
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
            const verticalCondition = state.currentBounds.west < station.lng && state.currentBounds.east > station.lng;
            const horizontalCondition = state.currentBounds.south < station.lat && state.currentBounds.north > station.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
    },
    searchStations: (state: State, getters: any) =>{
        const stations: Station[] = [];
        getters.lines.forEach((line: Line) => {
            line.stations.forEach(station => {
                if (station.name.indexOf(state.searchWord) > -1) {
                    stations.push(station)
                }
            });
        });
        return state.searchWord?getters.removeOverlap(stations):[];
    },
    removeOverlap: (state:State) =>(stations: Station[]) =>{
        let map = new Map(stations.map(station => [station.name, station]));
        return Array.from(map.values());
    },
    stationInfo(state: State){return state.stationInfo},
}

const mutations = {
    setCompanies(state: State, payload: Company[]){
        // payload.forEach(company => {
        //     state.companies.push(company);
        // });
    },
    selectedCompanyItems(state: State, payload: Company[]){
        state.selectedCompanyItems = payload;
    },
    selectedLineItems(state: State, payload: Line[]){
        state.selectedLineItems = payload;
    },
    clearItem(state: State, payload: number){
        state.selectedCompanyItems.splice(payload,1);
    },
    map(state: State, payload: any){
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
    uncheck(state: State, payload: Line[]){
        if(payload.length == 1){
            state.selectedLineItems = state.selectedLineItems.filter((item)=>{
                return item.company_id !== payload[0].id;
            })
        } else {
            state.selectedLineItems = [];
        }
    }
};

const actions = {
    async getCompanies(context: any){
        // const response = await $axios.$get('/api/map/');
        // context.commit('setCompanies', response);
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
    selectedCompanyItems(context: any, payload: {name: string, text: string}[]){
        context.commit('selectedCompanyItems', payload)
    },
    selectedLineItems(context: any, payload: {name: string, text: string}[]){
        context.commit('selectedLineItems', payload)
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
        let err, response = await $axios.$get('/api/map/station/line/wiki/',{params:payload});
        if(err){
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('stationInfo', response)
    },
    uncheck(context: any, payload: string){
        context.commit('uncheck', payload)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
