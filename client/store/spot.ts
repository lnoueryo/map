import { $axios } from '~/utils/api';

interface State {
    fields: string[]
    prefectures: Prefecture[],
    population: { city: string, population: number[] },
    selectedPrefectureItems: Prefecture[],
    selectedCityItems: City[],
    currentBounds: Bounds,
    selectedMarker: City
    searchWord: string,
    addressElement: null | AddressElement[],
    query: Query
    params: Params | null,
    spot: Spot
    searchResult: Town[],
}
interface Coordinate { lat: number, lng: number };
interface Polygon { lat: number, lng: number }[];
interface Bounds { north: number, south: number, west: number, east: number };
interface AddressElement { Code: string, Name: string, Kana: string, Level: string }
interface Prefecture { id: string, name: string, lat: number, lng: number, cities: City[] }
interface City { id: string, name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: Spot[], polygons: Polygon[][], prefecture_id: string }
interface Town { name: string, address: string, lat: string, lng: string, city_code: string }
interface Query { prefecture_id: string, city_code: string }
interface Spot { id: number, name: string, place_id: string, address: string, lat: string, lng: string, city_code: string }
interface Params { prefecture_id: string, city_code: string, id: number }

const getDefaultState = () => {
    return {
        prefectures: [],
        currentBounds: { south: 0, north: 0, east: 0, west: 0 },
        searchResult: [],
        addressElement: null,
        query: {},
        params: null,
        spot: {}
    }
}

const state = () => getDefaultState();

const getters = {
    prefectures: (state: State) => state.prefectures,
    cities: (state: State, getters: any) => {
        const cities = [].concat(...getters.prefectures.map((prefecture: Prefecture): City[] => prefecture.cities));
        return cities ?? [];
    },
    spots: (state: State, getters: any) => {
        const spots = [].concat(...getters.cities.map((city: City): Spot[] => city?.spots));
        return spots;
    },
    query: (state: State) => state.query,
    filterPrefectures: (state: State) => {
        let result = JSON.parse(JSON.stringify(state.prefectures));
        if('prefecture_id' in state.query && result.length !== 0) {
            result = result.find((prefecture: Prefecture) => prefecture.id == state.query.prefecture_id);
            if('city_code' in state.query) {
                result = result.cities.find((city: City) => city.id == state.query.city_code);
            }
        }
        return result;
    },
    searchResult: (state: State): Town[] => state.searchResult,
    boundsFilter: (state: State) => (points: Coordinate[]): Coordinate[] => { //現在表示されているマップ内にあるマーカー(駅)のみ返す
        if(!Array.isArray(points)) return [];
        const filteredStations = points.filter((point) => {
            const verticalCondition = state.currentBounds.west < point.lng && state.currentBounds.east > point.lng;
            const horizontalCondition = state.currentBounds.south < point.lat && state.currentBounds.north > point.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
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
    boundsFilteredLists: (state: State, getters: any) => {
        let result;
        if ('prefecture_id' in state.query && 'city_code' in state.query) {
            result = getters.spots.filter((spot: Spot) => {
                return spot.city_code == state.query.city_code;
            })
        } else if ('prefecture_id' in state.query) {
            result = getters.cities.filter((city: City) => {
                return city?.prefecture_id == state.query.prefecture_id;
            })
        } else {
            result = getters.prefectures;
        }
        return getters.boundsFilter(result);
    },
    showNumberOfMarkers: (state: State, getters: any): number => { //現在表示されているマーカーの数を返す
        return getters.boundsFilteredLists.length;
    },
    searchSpots: (state: State, getters: any): Spot[] => { //検索バーに入った駅名がstationにあればオブジェクトを返す
        const spots = getters.spots.filter((spot: Spot) => spot?.name.indexOf(state.searchWord) > -1);
        return state.searchWord && spots ? spots : [];
    },
    // detail-page
    spot: (state: State, getters: any) => state.spot,
}

const mutations = {
    resetState: (state: State) => {
        Object.assign(state, getDefaultState())
    },
    currentBounds: (state: State, payload: Bounds) => {
        state.currentBounds = { ...state.currentBounds, ...payload }
    },
    searchResult: (state: State, payload: Town[]) => {
        state.searchResult = payload;
    },
    addressElement: (state: State, payload: AddressElement[]) => {
        state.addressElement = payload;
    },
    query: (state: State, payload: Query) => {
        state.query = payload;
    },
    prefectures: (state: State, payload: Prefecture[]) => {
        state.prefectures = payload;
    },
    // detail-page
    params: (state: State, payload: Params) => {
        state.params = payload;
    },
    spot: (state: State, payload: Spot) => {
        state.spot = payload;
    },
};

const actions = {
    getPrefectures: async (context: any) => {
        const response = await $axios.$get('/api/prefecture/city/');
        context.commit('prefectures', response)
    },
    getCity: async (context: any, payload: { mapCenter: Coordinate, zoom: number }) => {
        const response = await $axios.$get('/api/search-by-reverse-geocode/', { params: payload.mapCenter });
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
    query: (context: any, payload: Query) => {
        context.commit('query', payload)
    },
    getCurrentBounds: (context: any, payload: Bounds) => {
        context.commit('currentBounds', payload)
    },
    searchWord: (context: any, payload: string) => {
        context.commit('searchWord', payload)
    },
    params: (context: any, payload: Params) => {
        context.commit('params', payload)
    },
    getSpot: async (context: any, payload: {prefecture_id: string, city_code: string, id: string}) => {
        const response = await $axios.$get('/api/spot/', { params: {id: payload.id} });
        context.commit('spot', response)
        const twitterQuery = {name: response.name, lat: response.lat, lng: response.lng}
        context.dispatch('info/getTwitterInfo', twitterQuery, {root: true})
        context.dispatch("info/getAroundSpot", twitterQuery, {root: true});
    },
    searchTown: async(context: any, payload: string) => {
        if(payload) {
            const response = await $axios.$get('/api/search/town/', {params: {word: payload}})
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