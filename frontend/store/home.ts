import { $axios } from '~/utils/api';
import companies from '~/assets/json/company.json';
import cities from '~/assets/json/cities.json';
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
        cities: Cities[],
        selectCities: number[]
    }
interface Polygon {lat: number, lng: number}[]
interface Bounds {north: number, south: number, west: number, east: number};
interface Company {id: number, name: string, address: string, founded: string, lines: Line[]};
interface Line {id: number, company_id: number, name: string, polygon: Polygon, color: string,stations: Station[]};
interface Station {name: string,id:number,line_id:number,order:number,prefecture:string,lat:number,lng:number,company_id:number,city_code: string}
interface Cities {prefecture_id: number, city_code: number, city: string, polygons:Polygon[][]}

const state = {
    companies: [],
    selectedCompanyItems: [],
    selectedLineItems: [],
    map: null,
    currentBounds: {south: 0, north: 0,east: 0, west: 0},
    markerSwitch: true,
    lineSwitch: true,
    selectedMarker: {},
    searchWord: null,
    stationInfo: null,
    cities: cities,
    selectCities: []
};

const getters = {
    /*
    フィルタリングされていない会社,路線図,駅データ全ての配列
    現在データベースからではなくjsonファイルから読み込んでいる
    */
    companies:(state: State): Company[]=>{return companies;},
    /*
    フィルタリングされていない市町村ポリゴンを返す
    */
    cities:(state: State): Cities[]=>{return cities;},
    /*
    company配列より路線図のみを抽出し、
    選択された会社名でフィルタリングされた配列を返す
    */
    lineItems:(state: State, getters: any)=>{
        const lines = [].concat(...getters.companies.map((company: Company): Line[]=>{
            return (company.lines)
        }));
        return getters.companyFilter(lines);
    },
    /*
    company配列より路線図のみを抽出し、
    選択された全ての要素でフィルタリングされた配列を返す
    */
    lines:(state: State, getters: any)=>{
        const lines = [].concat(...getters.companies.map((company: Company): Line[]=>{
            return (company.lines)
        }));
        return getters.filteredLines(lines);
    },
    /*
    会社->路線図の順でフィルタリングする
    */
    filteredLines:(state: State, getters: any)=>(lines: Line[]) =>{
        // let filteredLines = getters.companyFilter(lines);
        // filteredLines = getters.lineFilter(filteredLines);
        // return filteredLines;
        return getters.cityFilter(lines);
    },
    /*
    選択された会社のフィルター
    選択されたcompanyのpkとlinesのcompany_idが一致したオブジェクトを返す
    */
    companyFilter: (state: State) => (lines: Line[]): Line[ ] => {
        const companyIds = state.selectedCompanyItems.map((selectedCompanyItem)=>{ //選択された会社のid
            return selectedCompanyItem.id
        })
        let selectedLines;
        if (state.selectedCompanyItems.length!==0) {//会社が選択されてる場合
            selectedLines = lines.filter((line)=>{
                return companyIds.includes(line.company_id);
            });
        } else { //会社が選択されていない場合
            selectedLines = lines;
        }
        return selectedLines;
    },
    /*
    選択された路線図のフィルター
    選択されたlineのpkとlinesのidが一致したオブジェクトを返す
    */
    lineFilter: (state: State) => (lines: Line[]) => {//選択された路線図のフィルター
        const lineIds = state.selectedLineItems.map((selectedLineItem)=>{ //選択された路線図のid
            return selectedLineItem.id
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
    /*
    選択された路線図のフィルター
    選択されたlineのpkとlinesのidが一致したオブジェクトを返す
    */
    cityFilter: (state: State, getters: any) => (lines: Line[]) => {//選択された路線図のフィルター
        return getters.selectedCities.length == 0? lines : lines.map((line)=>{
            line.stations = line.stations.filter((station)=>{
                return getters.selectedCities.filter((selectedCity: number)=>{
                    return Number(selectedCity) == Number(station.prefecture+station.city_code)
                }).length !== 0;
            })
            return line;
        })
    },
    selectedCompanyItems: (state: State): Company[] => {return state.selectedCompanyItems;},
    selectedLineItems: (state: State): Line[] => {return state.selectedLineItems;},
    searchWord: (state: State): string => {return state.searchWord;},
    bounds: (state: State): Bounds => {return state.currentBounds;}, //現在のマップのサイズを緯度経度のオブジェクトで返す
    markerSwitch: (state: State): boolean =>{return state.markerSwitch;}, //マーカー表示のboolean
    lineSwitch: (state: State) => {return state.lineSwitch;}, //路線図表示のboolean
    selectedMarker: (state: State): Station => {return state.selectedMarker;}, //クリックされたマーカー(駅)のオブジェクトを返す
    showNumberOfMarkers: (state: State, getters: any): number =>{ //現在表示されているマーカーの数を返す
        return getters.lines.reduce((sum:any, line:any): number => {
            return sum + (getters.boundsFilter(line.stations)).length;
        }, 0);
    },
    boundsFilter: (state:State) =>(stations: Station[]): Station[] =>{ //現在表示されているマップ内にあるマーカー(駅)のみ返す
        const filteredStations = stations.filter((station)=>{
            const verticalCondition = state.currentBounds.west < station.lng && state.currentBounds.east > station.lng;
            const horizontalCondition = state.currentBounds.south < station.lat && state.currentBounds.north > station.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
    },
    searchStations: (state: State, getters: any): Station[] =>{ //検索バーに入った駅名がstationにあればオブジェクトを返す
        const stations = [].concat(...getters.lines.map((line: Line)=>{
            return line.stations;
        })).filter((station: Station)=>{return station.name.indexOf(state.searchWord) > -1});
        return state.searchWord?getters.removeOverlap(stations):[];
    },
    removeOverlap: (state:State) =>　(stations: Station[]) =>{ //重複した駅名を削除
        let map = new Map(stations.map(station => [station.name, station]));
        return Array.from(map.values());
    },
    stationInfo(state: State){return state.stationInfo}, //ウィキから引っ張ってきたhtmlを返す
    selectedCities(state: State){return state.selectCities}, //ウィキから引っ張ってきたhtmlを返す
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
    },
    selectCity(state: State, payload: number){
        const index = state.selectCities.findIndex((selectCity)=>{
            return selectCity == payload;
        });
        if (index==-1) {
            state.selectCities.push(payload);
        } else {
            state.selectCities.splice(index, 1);
        }
        console.log(1)
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
    async searchCityCode(context: any,payload: google.maps.MapMouseEvent){
        // const latLng = {lat: payload.latLng?.lat(), lng: payload.latLng?.lng()};
        // const response = await $axios.$post('/api/map/search-by-reverse-geocode', latLng);
        // context.commit('selectCity', response.Property.AddressElement[1].Code);
        // context.commit('selectCity', payload);
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
