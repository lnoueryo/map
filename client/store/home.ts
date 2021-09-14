import { $axios } from '~/utils/api';
import prefectures from '~/assets/json/city.json';
import population from '../assets/json/population.json'

interface State {
    fields: string[]
    prefectures: City[],
    population: { city: string, population: number[] },
    selectedPrefectureItems: Prefecture[],
    selectedCityItems: City[],
    currentBounds: Bounds,
    selectedMarker: City
    searchWord: string,
    addressElement: null | AddressElement[],
}
interface Coordinate { lat: number, lng: number };
interface Polygon { lat: number, lng: number }[];
interface Bounds { north: number, south: number, west: number, east: number };
interface AddressElement { Code: string, Name: string, Kana: string, Level: string }
interface Prefecture { id: string, name: string, lat: number, lng: number, cities: City[] }
interface City { name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: Spot[], polygons: Polygon[][] }
interface Spot { name: string, place_id: string, address: string, lat: string, lng: string }

const state = {
    fields: ['prefectures', 'cities', 'spots'],
    prefectures: prefectures,
    population: population,
    selectedPrefectureItems: [],
    selectedCityItems: [],
    currentBounds: { south: 0, north: 0, east: 0, west: 0 },
    selectedMarker: {},
    searchWord: null,
    addressElement: null,
};

const getters = {
    fields: (state: State) => state.fields,
    /*
    フィルタリングされていない人口情報を返す
    */
    population: (state: State) => state.population,
    prefectures: (state: State) => state.prefectures,
    cities: (state: State, getters: any) => {
        const cities = [].concat(...getters.prefectures.map((prefecture: Prefecture): City[] => prefecture.cities));
        return cities;
    },
    spots: (state: State, getters: any) => {
        const spots = [].concat(...getters.cities.map((city: City): Spot[] => city.spots));
        return spots;
    },
    selectedPrefectureItems: (state: State): Prefecture[] => state.selectedPrefectureItems,
    selectedCityItems: (state: State): City[] => state.selectedCityItems,
    searchWord: (state: State): string => state.searchWord,
    selectedMarker: (state: State): City => state.selectedMarker, //クリックされたマーカー(駅)のオブジェクトを返す
    boundsFilter: (state: State) => (points: Coordinate[]): Coordinate[] => { //現在表示されているマップ内にあるマーカー(駅)のみ返す
        const filteredStations = points.filter((point) => {
            const verticalCondition = state.currentBounds.west < point.lng && state.currentBounds.east > point.lng;
            const horizontalCondition = state.currentBounds.south < point.lat && state.currentBounds.north > point.lat;
            return verticalCondition && horizontalCondition;
        });
        return filteredStations;
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
}

const mutations = {
    selectedPrefectureItems: (state: State, payload: Prefecture[]) => {
        state.selectedPrefectureItems = payload;
    },
    currentBounds: (state: State, payload: Bounds) => {
        state.currentBounds = { ...state.currentBounds, ...payload }
    },
    selectMarker: (state: State, payload: City) => {
        state.selectedMarker = { ...state.selectedMarker, ...payload };
    },
    searchWord: (state: State, payload: string) => {
        state.searchWord = payload;
    },
    addressElement: (state: State, payload: AddressElement[]) => {
        state.addressElement = payload;
    },
};

const actions = {
    selectedPrefectureItems: (context: any, payload: Prefecture[]) => {
        context.commit('selectedPrefectureItems', payload)
    },
    getCurrentBounds: (context: any, payload: Bounds) => {
        context.commit('currentBounds', payload)
    },
    selectMarker: (context: any, payload: City) => {
        context.commit('selectMarker', payload)
    },
    searchWord: (context: any, payload: string) => {
        context.commit('searchWord', payload)
    },
    getCity: async (context: any, payload: { mapCenter: Coordinate, zoom: number }) => {
        const response = await $axios.$get('/api/search-by-reverse-geocode/', { params: payload.mapCenter });
        // const response = await $axios.$post('/api/search-by-reverse-geocode/', payload.mapCenter);
        console.log(response)
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
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}