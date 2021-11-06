import { $axios } from '~/utils/api';
// import cities from '../assets/json/city.json'
// import addresses from '../assets/json/addresses.json'
// import facilities from '../assets/json/city_facility.json'
// import occupations from '../assets/json/city_occupation.json'
// import populations from '../assets/json/city_population.json'
// import stations from '../assets/json/stations.json'
// import lines from '../assets/json/lines.json'
// import companies from '../assets/json/companies.json'
// import lineStations from '../assets/json/line_stations.json'
// import analysisData from '~/assets/json/analyzed_column_json/13.json'
interface State {
    prefectures: Prefecture[]
    cities: Prefecture,
    city: City
}
interface Prefecture { id: string, name: string, lat: number, lng: number };
interface Coordinate { lat: number, lng: number };
interface Spot { id: number, name: string, place_id: string, address: string, lat: number, lng: number, prefecture_id: string, city_code: string, geohash: string }
interface Polygon { lat: number, lng: number }[];
interface Bounds { north: number, south: number, west: number, east: number };
interface Company { id: number, name: string, address: string, founded: string, lines: Line[] };
interface Line { id: number, company_id: number, name: string, polygon: Polygon, color: string, stations: Station[] };
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string }
interface AddressElement { Code: string, Name: string, Kana: string, Level: string }
interface City { name: string, city_code: string, province: string, lat: string, lng: string, city: string, spots: { name: string, place_id: string, address: string, lat: string, lng: string }, polygons: Polygon[][] }
interface Address { id: number, name: string, city_code: string, prefecture_id: string, lat: string, lng: string, geohash: string }
interface Station { name: string, id: number, line_id: number, order: number, prefecture: string, lat: number, lng: number, company_id: number, city_code: string, lines: any }
interface LineStations { id: number, station_id: number, line_id: number }

const state = {
    prefectures: [],
    cities: {},
    city: {},
};

const getters = {
    prefectures: (state: State) => state.prefectures,
    cities: (state: State) => state.cities,
    city: (state: State) => state.city,
}

const mutations = {
    prefectures: (state: State, payload: Prefecture[]) => {
        state.prefectures = payload;
    },
    cities: (state: State, payload: Prefecture) => {
        state.cities = payload;
    },
    city: (state: State, payload: City) => {
        state.city = payload;
    },
};

const actions = {
    getPrefectures: async(context: any) => {
        try {
            const response = await $axios.$get('/api/prefecture/city/');
            context.commit('prefectures', response);
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection')
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    getCities: async(context: any, payload: {city_code: string}) => {
        try {
            const response = await $axios.$get('/api/prefecture/city/', {params: payload});
            context.commit('cities', response)
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection')
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    getCity: async(context: any, payload: {city_code: string}) => {
        try {
            const response = await $axios.$get('/api/city/', {params: payload});
            context.commit('city', response)
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection')
            else context.dispatch('errorDialog', true, { root: true })
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
