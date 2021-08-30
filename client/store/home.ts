import { $axios } from '~/utils/api';
import companies from '~/assets/json/company.json';
import cities from '~/assets/json/city.json';
import population from '../assets/json/population.json'


interface State {
    companies: Company[]
    selectedCompanyItems: Company[],
    selectedLineItems: Line[],
    selectedCityItems: City[],
    map: any,
    currentBounds: Bounds,
    markerSwitch: boolean,
    lineSwitch: boolean,
    chartSwitch: boolean,
    dotSwitch: boolean,
    selectedMarker: Station,
    searchWord: string,
    changeList: number,
    stationInfo: null|string,
    cityWikiInfo: null|string,
    twitterInfo: Twitter[],
    cities: City[],
    searching: boolean,
    addressElement: null | AddressElement[],
    population: {city: string, population: number[]},
    lineChartIndex: number,
    events: string[],
    stationSwitch: boolean,
    citySwitch: boolean,
    spotSwitch: boolean,
}
interface Coordinate {lat: number, lng: number};
interface Polygon {lat: number, lng: number}[];
interface Bounds {north: number, south: number, west: number, east: number};
interface Company {id: number, name: string, address: string, founded: string, lines: Line[]};
interface Line {id: number, company_id: number, name: string, polygon: Polygon, color: string,stations: Station[]};
interface Station {name: string,id:number,line_id:number,order:number,prefecture:string,lat:number,lng:number,company_id:number,city_code: string}
// interface City {prefecture_id: string, city_code: string, city: string, polygons:Polygon[][]}
interface AddressElement {Code: string, Name: string, Kana: string, Level: string}
interface Twitter {id: number, 'name': string, 'profile_image_url': string, 'followers_count': number, 'friends_count': number, 'text': string, 'images': string[]}
interface City   {name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: {name: string, place_id: string, address: string, lat: string, lng: string}, polygons:Polygon[][]}

const state = {
    companies: companies,
    cities: cities,
    population: population,
    selectedCompanyItems: [],
    selectedLineItems: [],
    selectedCityItems: [],
    map: null,
    currentBounds: {south: 0, north: 0,east: 0, west: 0},
    selectedMarker: {},
    searchWord: null,
    changeList: 0,
    stationInfo: null,
    cityWikiInfo: null,
    twitterInfo: [],
    searching: false,
    addressElement: null,
    lineChartIndex: 0,
    events: [],
    markerSwitch: true,
    lineSwitch: true,
    chartSwitch: false,
    dotSwitch: true,
    stationSwitch: true,
    citySwitch: true,
    spotSwitch: true,
};

const getters = {
    /*
    フィルタリングされていない会社,路線図,駅データ全ての配列
    現在データベースからではなくjsonファイルから読み込んでいる
    */
    companies: (state: State): Company[] => state.companies,
    /*
    フィルタリングされていない人口情報を返す
    */
    population: (state: State) => state.population,
    events: (state: State) => state.events,
    /*
    company配列より路線図のみを抽出し、
    選択された会社名でフィルタリングされた配列を返す
    */
   lineItems: (state: State, getters: any) => {
       const lines = [].concat(...getters.companies.map((company: Company): Line[] => company.lines));
       return getters.companyFilter(lines);
    },
    originalCities: (state: State, getters: any) => {
        return state.cities
    },
    cities: (state: State, getters: any) => {
        return state.spotSwitch ? getters.cityFilterForCities(state.cities) : []
    },
    /*
    company配列より路線図のみを抽出し、
    選択された全ての要素でフィルタリングされた配列を返す
    */
    lines: (state: State, getters: any) => {
        const lines = [].concat(...getters.companies.map((company: Company): Line[] => company.lines));
        const filteredLines = getters.filteredLines(lines);
        return filteredLines;
    },
    /*
    会社->路線図の順でフィルタリングする
    */
    filteredLines: (state: State, getters: any) => (lines: Line[]) => {
        let filteredLines = getters.companyFilter(lines);
        filteredLines = getters.lineFilter(filteredLines);
        filteredLines = getters.cityFilter(filteredLines);
        return filteredLines;
    },
    /*
    選択された会社のフィルター
    選択されたcompanyのpkとlinesのcompany_idが一致したオブジェクトを返す
    */
    companyFilter: (state: State) => (lines: Line[]): Line[] => {
        const companyIds = state.selectedCompanyItems.map((selectedCompanyItem) => { //選択された会社のid
            return selectedCompanyItem.id
        })
        let selectedLines = state.selectedCompanyItems.length !== 0
                          ? lines.filter((line) => companyIds.includes(line.company_id))
                          : lines
        return selectedLines;
    },
    /*
    選択された路線図のフィルター
    選択されたlineのpkとlinesのidが一致したオブジェクトを返す
    */
    lineFilter: (state: State) => (lines: Line[]) => {//選択された路線図のフィルター
        const lineIds = state.selectedLineItems.map((selectedLineItem) => { //選択された路線図のid
            return selectedLineItem.id
        })
        let selectedLines = state.selectedLineItems.length !== 0
                          ? lines.filter((line) => lineIds.includes(line.id))
                          : lines
        return selectedLines;
    },
    /*
    選択された地域のフィルター
    選択された地域のコードとstationsのcity_codeが一致したオブジェクトを返す
    二次元配列をmapで扱うためdeepcopyを使う
    */
    cityFilter: (state: State, getters: any) => (lines: Line[]) => {//選択された路線図のフィルター
        const cityCodes = state.selectedCityItems.map((selectedCityItem) => { //選択された路線図のid
            const code = selectedCityItem.city_code;
            return code;
        })
        let copyLines: Line[] = JSON.parse(JSON.stringify(lines));
        return getters.selectedCities.length == 0 ? copyLines : copyLines.map((line) => {
            line.stations = line.stations.filter((station) => {
                return cityCodes.includes(station.city_code);
            })
            return line;
        })
    },
    cityFilterForCities: (state: State, getters: any) => (cities: City[]) => {//選択された路線図のフィルター
        const cityCodes = state.selectedCityItems.map((selectedCityItem) => { //選択された路線図のid
            const code = selectedCityItem.city_code;
            return code;
        })
        let copyCities: City[] = JSON.parse(JSON.stringify(cities));
        return getters.selectedCities.length == 0 ? copyCities : copyCities.filter((city) => {
            return cityCodes.includes(city.city_code);
        })
    },
    selectedCompanyItems: (state: State): Company[] => state.selectedCompanyItems,
    selectedLineItems: (state: State): Line[] => state.selectedLineItems,
    selectedCityItems: (state: State): City[] => state.selectedCityItems,
    searchWord: (state: State): string => state.searchWord,
    changeList: (state: State): number => state.changeList,
    markerSwitch: (state: State): boolean => state.markerSwitch, //マーカー表示のboolean
    lineSwitch: (state: State) => state.lineSwitch, //路線図表示のboolean
    chartSwitch: (state: State) => state.chartSwitch, //グラフ表示のboolean
    dotSwitch: (state: State) => state.dotSwitch, //ドット表示のboolean
    selectedMarker: (state: State): Station => state.selectedMarker, //クリックされたマーカー(駅)のオブジェクトを返す
    showNumberOfMarkers: (state: State, getters: any): number => { //現在表示されているマーカーの数を返す
        const stations = getters.lines.reduce((sum:any, line:any): number => sum + (getters.boundsFilter(line.stations)).length, 0)
        const spots = getters.cities.reduce((sum:any, city:any): number => sum + (getters.boundsFilter(city.spots)).length, 0)
        return getters.stationSwitch && getters.spotSwitch ? stations + spots : getters.stationSwitch ? stations : spots;
    },
    boundsFilter: (state: State) => (points: Coordinate[]): Coordinate[] => { //現在表示されているマップ内にあるマーカー(駅)のみ返す
        const filteredStations = points.filter((point) => {
            const verticalCondition = state.currentBounds.west < point.lng && state.currentBounds.east > point.lng;
            const horizontalCondition = state.currentBounds.south < point.lat && state.currentBounds.north > point.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
    },
    searchStations: (state: State, getters: any): Station[] => { //検索バーに入った駅名がstationにあればオブジェクトを返す
        const stations = [].concat(...getters.lines.map((line: Line) => {
            return line.stations;
        })).filter((station: Station) => station.name.indexOf(state.searchWord) > -1);
        return state.searchWord?getters.removeOverlap(stations):[];
    },
    removeOverlap: (state:State) =>(stations: Station[]) => { //重複した駅名を削除
        let map = new Map(stations.map(station => [station.name, station]));
        return Array.from(map.values());
    },
    stationInfo: (state: State) => state.stationInfo, //ウィキから引っ張ってきたhtmlを返す
    cityWikiInfo: (state: State) => state.cityWikiInfo, //ウィキから引っ張ってきたhtmlを返す
    twitterInfo: (state: State) => state.twitterInfo, //ツイッターから引っ張ってきたjsonを返す
    selectedCities: (state: State) => state.selectedCityItems, //ウィキから引っ張ってきたhtmlを返す
    searching: (state: State) => state.searching, //ウィキ検索中のloading処理
    removeAddressElement: (state: State) => (elements: AddressElement[], zoom: number) => {
        let index: number;
        if(8 <= zoom && 10 > zoom) index = 1;
        else if(10 <= zoom && 14 > zoom) index = 2;
        else if(14 <= zoom && 16 > zoom) index = 3;
        else if(16 <= zoom && 18 > zoom) index = 4;
        else if(18 <= zoom) index = 5;
        return elements.filter((element: AddressElement, i: number) => {
            return i < index;
        })
    },
    addressElement: (state: State) => state.addressElement,
    lineChartIndex: (state: State) => state.lineChartIndex,
    stationSwitch: (state: State) => state.stationSwitch,
    citySwitch: (state: State) => state.citySwitch,
    spotSwitch: (state: State) => state.spotSwitch,
}

const mutations = {
    setCompanies: (state: State, payload: Company[]) => {
        payload.forEach(company => state.companies.push(company));
    },
    selectedCompanyItems: (state: State, payload: Company[]) => {
        state.selectedCompanyItems = payload;
    },
    selectedLineItems: (state: State, payload: Line[]) => {
        state.selectedLineItems = payload;
    },
    selectedCityItems: (state: State, payload: City[]) => {
        state.selectedCityItems = payload;
    },
    clearItem: (state: State, payload: number) => {
        state.selectedCompanyItems.splice(payload, 1);
    },
    map: (state: State, payload: any) => {
        state.map = payload
    },
    currentBounds: (state: State, payload: Bounds) => {
        state.currentBounds = Object.assign({}, state.currentBounds,payload)
    },
    markerSwitch: (state: State, payload: boolean) => {
        state.markerSwitch = payload;
    },
    lineSwitch: (state: State, payload: boolean) => {
        state.lineSwitch = payload;
    },
    chartSwitch: (state: State, payload: boolean) => {
        state.chartSwitch = payload;
    },
    stationSwitch: (state: State, payload: boolean) => {
        state.stationSwitch = payload;
    },
    spotSwitch: (state: State, payload: boolean) => {
        state.spotSwitch = payload;
    },
    dotSwitch: (state: State, payload: boolean) => {
        state.dotSwitch = payload;
    },
    selectMarker: (state: State, payload: Station) => {
        state.selectedMarker = Object.assign({}, state.selectedMarker, payload);
    },
    searchWord: (state: State, payload: string) => {
        state.searchWord = payload;
    },
    changeList: (state: State, payload: number) => {
        state.changeList = payload;
    },
    stationInfo: (state: State, payload: string) => {
        state.stationInfo = payload;
    },
    cityWikiInfo: (state: State, payload: string) => {
        state.cityWikiInfo = payload;
    },
    twitterInfo: (state: State, payload: Twitter[]) => {
        state.twitterInfo = payload;
    },
    searching: (state: State, payload: boolean) => {
        state.searching = payload;
    },
    uncheck: (state: State, payload: Line[]) => {
        state.selectedLineItems = payload.length == 1
                                ? state.selectedLineItems.filter((item) => item.company_id !== payload[0].id)
                                : []
    },
    selectCityItems: (state: State, payload: City) => {
        const index = state.selectedCityItems.findIndex((selectCity) => {
            return selectCity.city_code == payload.city_code;
        });
        index == -1 ? state.selectedCityItems.push(payload) : state.selectedCityItems.splice(index, 1)
    },
    addressElement: (state: State, payload: AddressElement[]) => {
        state.addressElement = payload;
    },
    lineChartIndex: (state: State, payload: number) => {
        state.lineChartIndex = payload;
    },
    changeLineChartIndex: (state: State, payload: number) => {
        state.lineChartIndex += payload;
    },
    events: (state: State, payload: string[]) => {
        state.events = payload;
    },
};

const actions = {
    getCompanies: async(context: any) => {
        // const response = await $axios.$get('/api/');
        // console.log(response)
        // context.commit('setCompanies', response);
    },
    selectedCompanyItems: (context: any, payload: {name: string, text: string}[]) => {
        context.commit('selectedCompanyItems', payload)
    },
    selectedLineItems: (context: any, payload: {name: string, text: string}[]) => {
        context.commit('selectedLineItems', payload)
    },
    clearItem: (context: any, payload: number) => {
        context.commit('clearItem', payload);
    },
    getCurrentBounds: (context: any, payload: Bounds) => {
        context.commit('currentBounds', payload)
    },
    changeMarkerSwitch: (context: any, payload: boolean) => {
        context.commit('markerSwitch', payload)
    },
    changeLineSwitch: (context: any, payload: boolean) => {
        context.commit('lineSwitch', payload)
    },
    changeChartSwitch: (context: any, payload: boolean) => {
        context.commit('chartSwitch', payload)
    },
    changeStationSwitch: (context: any, payload: boolean) => {
        context.commit('stationSwitch', payload)
    },
    changeSpotSwitch: (context: any, payload: boolean) => {
        context.commit('spotSwitch', payload)
    },
    changeDotSwitch: (context: any, payload: boolean) => {
        context.commit('dotSwitch', payload)
    },
    selectMarker: (context: any, payload: Station) => {
        context.commit('selectMarker', payload)
    },
    searchWord: (context: any, payload: string) => {
        context.commit('searchWord', payload)
    },
    changeList: (context: any, payload: number) => {
        context.commit('changeList', payload)
    },
    getStationInfo: async(context: any, payload: string) => {
        context.commit('searching', true)
        let err, response = await $axios.$get('/api/wiki/',{params: payload});
        if(err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('stationInfo', response)
    },
    getTwitterInfo: async(context: any, payload: string) => {
        let err, response = await $axios.$get('/api/twitter/',　{params: payload});
        if(err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        console.log(response)
        context.commit('twitterInfo', response)
    },
    uncheck: (context: any, payload: string) => {
        context.commit('uncheck', payload)
    },
    searchCityCode: async(context: any,payload: google.maps.MapMouseEvent) => {
        const latLng = {lat: payload.latLng?.lat(), lng: payload.latLng?.lng()};
        const response = await $axios.$post('/api/search-by-reverse-geocode/', latLng);
        const city = context.getters.originalCities.find((city: City) => {
            return city.city_code == response.Property.AddressElement[1].Code;
        })
        const index = context.state.selectedCityItems.findIndex((selectCity: City) => {
            return selectCity.city_code == city.city_code;
        });
        if (index == -1) context.dispatch('getCityWikiInfo', {name: city.name})
        context.commit('selectCityItems', city);
    },
    getCity: async(context: any, payload: {mapCenter: Coordinate, zoom: number}) => {
        const response = await $axios.$post('/api/search-by-reverse-geocode/', payload.mapCenter);
        let AddressElement;
        if (response.Property) {
            try {
                AddressElement = context.getters.removeAddressElement(response.Property.AddressElement, payload.zoom);
                context.dispatch('lineChartIndex', response);
            } catch (error) {
                AddressElement = [response.Property.Country];
            }
            context.commit('addressElement', AddressElement);
        }
    },
    getCityWikiInfo: async(context: any, payload: string) => {
        // context.commit('searching', true)
        let err, response = await $axios.$get('/api/wiki/', {params: payload});
        if(err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('cityWikiInfo', response)
    },
    lineChartIndex: async(context: any, payload: any) => {
        const cityIndex = context.getters.population.findIndex((city: City) => {
            return city.name == payload.Property.AddressElement[1].Name;
        })
        if (cityIndex !== -1) context.commit('lineChartIndex', cityIndex);
    },
    getEvents: async(context: any) => {
        const response = await $axios.$get('/api/event/');
        context.commit('events', response);
        // context.commit('events', response.events);
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
