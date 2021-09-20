import { $axios } from '~/utils/api';
import prefectures from '~/assets/json/city.json';
import population from '../assets/json/population.json'
import joinCompanies from '../assets/json/company.json'
import stations from '../assets/json/stations.json'
import lines from '../assets/json/lines.json'
import companies from '../assets/json/companies.json'
import lineStations from '../assets/json/line_stations.json'

interface State {
    prefectures: City[],
    population: { city: string, population: number[] },
    joinCompanies: Company[]
    companies: Company[],
    lines: Line[]
    stations: Station
    lineStations: LineStations[]
    currentBounds: Bounds,
    addressElement: null | AddressElement[],
    params: Params | null
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
interface Params { prefecture_id: string, city_code: string, id: number }
const state = {
    prefectures: prefectures,
    population: population,
    joinCompanies: joinCompanies,
    companies: companies,
    lines: lines,
    stations: stations,
    lineStations: lineStations,
    currentBounds: { south: 0, north: 0, east: 0, west: 0 },
    addressElement: null,
    params: null
};

const getters = {
    population: (state: State) => state.population,
    prefectures: (state: State) => state.prefectures,
    joinCompanies: (state: State) => state.joinCompanies,
    companies: (state: State) => state.companies,
    lines: (state: State) => state.lines,
    stations: (state: State) => state.stations,
    cities: (state: State, getters: any) => {
        const cities = [].concat(...getters.prefectures.map((prefecture: Prefecture): City[] => prefecture.cities));
        return cities;
    },
    spots: (state: State, getters: any) => {
        const spots = [].concat(...getters.cities.map((city: City): Spot[] => city.spots));
        return spots;
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
    combineStationsWithLines: (state: State, getters: any) => {
        return getters.stations.map((station: Station) => {
            const lineIds = state.lineStations.filter((lineStation) => lineStation.station_id == station.id).map(lineStation => lineStation.line_id)
            const lines = getters.lines.filter((line: Line) => lineIds.includes(line.id))
            station['lines'] = lines;
            return station;
        })
    },
    spotInfo: (state: State, getters: any) => {
        return state.params ? getters.prefectures
            .find((prefecture: Prefecture) => {
                return state.params?.prefecture_id == prefecture.id;
            })
            .cities.find((city: City) => {
                return state.params?.city_code == city.city_code;
            })
            .spots.find((spot: Spot) => {
                return state.params?.id == spot.id;
            }) : null;
    }
}

const mutations = {
    addressElement: (state: State, payload: AddressElement[]) => {
        state.addressElement = payload;
    },
    params: (state: State, payload: Params) => {
        state.params = payload;
    },
};

const actions = {
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
    params: (context: any, payload: Params) => {
        context.commit('params', payload)
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}