import { $axios } from '~/utils/api';
import companies from '~/assets/json/company.json';
import cities from '~/assets/json/old_city.json';
import population from '../assets/json/population.json'

interface State {
    fields: string[]
    companies: Company[]
    cities: City[],
    selectedCompanyItems: Company[],
    selectedLineItems: Line[],
    selectedCityItems: City[],
    currentBounds: Bounds,
    selectedMarker: Station,
    searchWord: string,
    addressElement: null | AddressElement[],
    population: { city: string, population: number[] },
    lineChartIndex: number,
}
interface Coordinate { lat: number, lng: number };
interface Polygon { lat: number, lng: number }[];
interface Bounds { north: number, south: number, west: number, east: number };
interface Company { id: number, name: string, address: string, founded: string, lines: Line[] };
interface Line { id: number, company_id: number, name: string, polygon: Polygon, color: string, stations: Station[] };
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string }
interface AddressElement { Code: string, Name: string, Kana: string, Level: string }
interface City { name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: { name: string, place_id: string, address: string, lat: string, lng: string }, polygons: Polygon[][] }
interface Spot { id: number, name: string, place_id: string, address: string, lat: number, lng: number, prefecture_id: string, city_code: string, geohash: string }


const state = {
    fields: ['stations', 'cities', 'spots'],
    companies: companies,
    cities: cities,
    population: population,
    selectedCompanyItems: [],
    selectedLineItems: [],
    selectedCityItems: [],
    currentBounds: { south: 0, north: 0, east: 0, west: 0 },
    selectedMarker: {},
    searchWord: null,
    addressElement: null,
    lineChartIndex: 0,
};

const getters = {
    fields: (state: State) => state.fields,
    /*
    フィルタリングされていない会社,路線図,駅データ全ての配列
    現在データベースからではなくjsonファイルから読み込んでいる
    */
    companies: (state: State): Company[] => state.companies,
    /*
    フィルタリングされていない人口情報を返す
    */
    population: (state: State) => state.population,
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
    cities: (state: State, getters: any, rootState: any, rootGetters: any) => {
        return rootGetters['switch/markerSwitches'].spots ? getters.cityFilterForCities(state.cities) : []
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
    currentBounds: (state: State) => state.currentBounds,
    selectedMarker: (state: State): Station => state.selectedMarker, //クリックされたマーカー(駅)のオブジェクトを返す
    showNumberOfMarkers: (state: State, getters: any, rootState: any, rootGetters: any): number => { //現在表示されているマーカーの数を返す
        const stationNum = [].concat(...getters.lines.map((line: Line) => {
            return getters.boundsFilter(line.stations);
        })).map((station: Station) => station.name).filter((name, index, array) => array.indexOf(name) === index).length;

        const spotNum = [].concat(...getters.cities.map((city: City) => {
            return getters.boundsFilter(city.spots);
        })).map((spot: Spot) => spot.name).filter((name, index, array) => array.indexOf(name) === index).length;

        return rootGetters['switch/markerSwitches'].stations && rootGetters['switch/markerSwitches'].spots ? stationNum + spotNum : rootGetters['switch/markerSwitches'].stations ? stationNum : spotNum;
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
        return state.searchWord ? getters.removeOverlap(stations) : [];
    },
    removeOverlap: (state: State) => (stations: Station[]) => { //重複した駅名を削除
        let map = new Map(stations.map(station => [station.name, station]));
        return Array.from(map.values());
    },
    selectedCities: (state: State) => state.selectedCityItems, //ウィキから引っ張ってきたhtmlを返す
    removeAddressElement: (state: State) => (elements: AddressElement[], zoom: number) => {
        let index: number;
        if (8 <= zoom && 10 > zoom) index = 1;
        else if (10 <= zoom && 14 > zoom) index = 2;
        else if (14 <= zoom && 16 > zoom) index = 3;
        else if (16 <= zoom && 18 > zoom) index = 4;
        else if (18 <= zoom) index = 5;
        return elements.filter((element: AddressElement, i: number) => {
            return i < index;
        })
    },
    addressElement: (state: State) => state.addressElement,
    lineChartIndex: (state: State) => state.lineChartIndex,
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
    currentBounds: (state: State, payload: Bounds) => {
        state.currentBounds = Object.assign({}, state.currentBounds, payload)
    },
    selectMarker: (state: State, payload: Station) => {
        state.selectedMarker = Object.assign({}, state.selectedMarker, payload);
    },
    searchWord: (state: State, payload: string) => {
        state.searchWord = payload;
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
};

const actions = {
    selectedCompanyItems: (context: any, payload: { name: string, text: string }[]) => {
        context.commit('selectedCompanyItems', payload)
    },
    selectedLineItems: (context: any, payload: { name: string, text: string }[]) => {
        context.commit('selectedLineItems', payload)
    },
    getCurrentBounds: (context: any, payload: Bounds) => {
        context.commit('currentBounds', payload)
    },
    selectMarker: (context: any, payload: Station) => {
        context.commit('selectMarker', payload)
    },
    searchWord: (context: any, payload: string) => {
        context.commit('searchWord', payload)
    },
    uncheck: (context: any, payload: string) => {
        context.commit('uncheck', payload)
    },
    searchCityCode: async (context: any, payload: google.maps.MapMouseEvent) => {
        const latLng = { lat: payload.latLng?.lat(), lng: payload.latLng?.lng() };
        const response = await $axios.$post('/api/search-by-reverse-geocode/', latLng);
        const city = context.getters.originalCities.find((city: City) => {
            return city.city_code == response.Property.AddressElement[1].Code;
        })
        const index = context.state.selectedCityItems.findIndex((selectCity: City) => {
            return selectCity.city_code == city.city_code;
        });
        if (index == -1) context.dispatch('info/getCityWikiInfo', { name: city.name }, { root: true })
        // if (index == -1) context.dispatch('getCityWikiInfo', {name: city.name})
        context.commit('selectCityItems', city);
    },
    getCity: async (context: any, payload: { mapCenter: Coordinate, zoom: number }) => {
        const response = await $axios.$get('/api/search-by-reverse-geocode/', { params: payload.mapCenter });
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
    lineChartIndex: async (context: any, payload: any) => {
        const cityIndex = context.getters.population.findIndex((city: City) => {
            return city.city == payload.Property.AddressElement[1].Name;
        })
        if (cityIndex !== -1) context.commit('lineChartIndex', cityIndex);
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
