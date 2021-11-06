import { $axios } from '~/utils/api';
// import joinCompanies from '../assets/json/company.json'
// import stations from '../assets/json/stations.json'
// import lines from '../assets/json/lines.json'
// import companies from '../assets/json/companies.json'
// import lineStations from '../assets/json/line_stations.json'
// import cities from '~/assets/json/old_city.json';
interface State {
    prefectures: Prefecture[]
    lines: Line[]
    stations: Station[]
    currentBounds: Bounds,
    addressElement: null | AddressElement[],
    params: Params | null
    query: Query
    searchResult: Station[],
    particularStations: Station[]
}
interface Coordinate { lat: number, lng: number };
interface Polygon { lat: number, lng: number }[];
interface Company { id: number, name: string, address: string, founded: string, lines: Line[] };
interface Line { id: number, company_id: number, name: string, polygon: Polygon, color: string, stations: Station[] };
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string }
interface Bounds { north: number, south: number, west: number, east: number };
interface AddressElement { Code: string, Name: string, Kana: string, Level: string }
interface Prefecture { id: string, name: string, lat: number, lng: number, cities: City[] }
interface City { name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: Spot[], polygons: Polygon[][] }
interface Spot { id: number, name: string, place_id: string, address: string, lat: string, lng: string }
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string, lines: any }
interface LineStations { id: number, station_id: number, line_id: number }
interface Params { prefecture_id: string, city_code: string, id: number, name: string, company_id: string }
interface Query { company_id: string, line_id: string }
const getDefaultState = () => {
    return {
        prefectures: [],
        lines: [],
        stations: [],
        currentBounds: { south: 0, north: 0, east: 0, west: 0 },
        addressElement: null,
        params: {},
        query: {},
        searchResult: [],
        particularStations: []
    }
}

const state = () => getDefaultState();
// const state = {
//     prefectures: [],
//     lines: [],
//     stations: [],
//     currentBounds: { south: 0, north: 0, east: 0, west: 0 },
//     addressElement: null,
//     params: {},
//     query: {},
//     searchResult: [],
//     particularStations: []
// };

const getters = {
    params: (state: State) => state.params,
    prefectures: (state: State) => state.prefectures,
    lines: (state: State, getters: any) => {
        return state.lines;
    },
    stations: (state: State) => state.stations,
    uniqueStations: (state: State, getters: any) => {
        const map = new Map(getters.stations.map((station: Station) => [station.name, station]));
        return Array.from(map.values());
    },
    particularStations: (state: State) => state.particularStations,
    filteredCompanyLines: (state: State, getters: any) => {
        let companies: Company[] = [];
        if (getters.params?.name) {
            const selectedStations = getters.particularStations.filter((station: Station) => station.name == getters.params?.name)
            const lineIds = selectedStations.map((station: Station) => {
                return station.lines.map((line: Line) => {
                    return line.id;
                })
            })
        }
        return companies
    },
    boundsFilteredStations: (state: State, getters: any) => {
        if (getters.particularStations) {
            const lines = [].concat(...getters.particularStations.map((station: Station) => station.lines));
            const filteredStations = [].concat(...lines.map((line: any) => line.stations));
            const stations = filteredStations.filter((station: Station) => {
                if('line_id' in state.query) {
                    return String(station.line_id) == state.query.line_id;
                } else if('company_id' in state.query) {
                    return String(station?.company_id) == (state.query as Query).company_id;
                }
                return true;
            })
            const map = new Map(stations.map((station: Station) => [station?.name, station]));
            return getters.boundsFilter(Array.from(map.values()))
        }
        return []
    },
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
    filteredStation: (state: State, getters: any) => {
        let stations = JSON.parse(JSON.stringify(getters.particularStations))
        if ('company_id' in state.query) {
            const companyIdsArray = (state.query.company_id as string).split(',')
            stations = stations.filter((station: Station) => {
                return companyIdsArray.includes(String(station.company_id));
            })
            if ('line_id' in state.query) {
                const lineIdsArray = (state.query.line_id as string).split(',')
                const stationsWithLine = stations.map((station: Station) => {
                    const lines = station.lines.filter((line: Line) => {
                        return lineIdsArray.includes(String(line.id));
                    })
                    if (lines.length !== 0) {
                        station.lines = lines;
                    }
                    return station
                })
                if (stationsWithLine.length !== 0) stations = stationsWithLine;
            }
        }
        return stations;
    },
    // lineItems: (state: State, getters: any) => {
    //     const lines = [].concat(...getters.companies.map((company: Company): Line[] => company.lines));
    //     return getters.companyFilter(lines);
    // },
    // originalCities: (state: State, getters: any) => {
    //     return state.cities
    // },
    searchResult: (state: State): Station[] => state.searchResult,
    currentBounds: (state: State) => state.currentBounds,
    showNumberOfMarkers: (state: State, getters: any): number => { //現在表示されているマーカーの数を返す
        return 'prefecture_id' in getters.params ? getters.boundsFilter(getters.uniqueStations).length : getters.boundsFilter(getters.prefectures).length;
    },
    boundsFilter: (state: State) => (points: Coordinate[]): Coordinate[] => { //現在表示されているマップ内にあるマーカー(駅)のみ返す
        const filteredStations = points.filter((point) => {
            const verticalCondition = state.currentBounds.west < point.lng && state.currentBounds.east > point.lng;
            const horizontalCondition = state.currentBounds.south < point.lat && state.currentBounds.north > point.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
    },
    removeOverlap: (state: State) => (stations: Station[]) => { //重複した駅名を削除
        let map = new Map(stations.map(station => [station.name, station]));
        return Array.from(map.values());
    },
}

const mutations = {
    resetState: (state: State) => {
        Object.assign(state, getDefaultState())
    },
    addressElement: (state: State, payload: AddressElement[]) => {
        state.addressElement = payload;
    },
    params: (state: State, payload: Params) => {
        state.params = payload;
    },
    query: (state: State, payload: Query) => {
        state.query = payload;
    },
    // setCompanies: (state: State, payload: Company[]) => {
    //     payload.forEach(company => state.companies.push(company));
    // },
    currentBounds: (state: State, payload: Bounds) => {
        state.currentBounds = Object.assign({}, state.currentBounds, payload)
    },
    searchResult: (state: State, payload: Station[]) => {
        state.searchResult = payload;
    },
    prefectures: (state: State, payload: Prefecture[]) => {
        state.prefectures = payload;
    },
    stations: (state: State, payload: Station[]) => {
        state.stations = payload;
    },
    particularStations: (state: State, payload: Station[]) => {
        state.particularStations = payload;
    },
    lines: (state: State, payload: Line[]) => {
        state.lines = payload;
    },
};

const actions = {
    getCity: async (context: any, payload: { mapCenter: Coordinate, zoom: number }) => {
        const response = await $axios.$get('/api/search-by-reverse-geocode/', { params: payload.mapCenter });
        // const response = await $axios.$post('/api/search-by-reverse-geocode/', payload.mapCenter);
        let AddressElement;
        if (response.Property) {
            try {
                AddressElement = context.getters.removeAddressElement(response.Property.AddressElement, payload.zoom);
            } catch (error) {
                AddressElement = [response.Property.Country];
            }
            context.commit('addressElement', AddressElement);
        }
    },
    params: (context: any, payload: Params) => {
        context.commit('params', payload)
    },
    query: (context: any, payload: Params) => {
        context.commit('query', payload)
    },
    getCurrentBounds: (context: any, payload: Bounds) => {
        context.commit('currentBounds', payload)
    },
    searchWord: (context: any, payload: string) => {
        context.commit('searchWord', payload)
    },
    getPrefectures: async (context: any) => {
        const response = await $axios.$get('/api/prefecture/');
        context.commit('prefectures', response)
    },
    getStations: async (context: any, payload: {prefecture_id: string}) => {
        const response = await $axios.$get('/api/station/', {params: payload});
        context.commit('stations', response)
    },
    getParticularStations: async (context: any, payload: {prefecture_id: string}) => {
        const response = await $axios.$get('/api/station/', {params: payload});
        context.commit('particularStations', response)
    },
    getLines: async (context: any, payload: {prefecture_id: string}) => {
        const response = await $axios.$get('/api/line/', {params: payload});
        context.commit('lines', response)
    },
    searchStation: async(context: any, payload: string) => {
        if(payload) {
            const response = await $axios.$get('/api/search/station/', {params: {word: payload}})
            context.commit('searchResult', response)
        } else {
            context.commit('searchResult', [])
        }
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}