import { $axios } from '~/utils/api';
import cities from '../assets/json/city.json'
import addresses from '../assets/json/addresses.json'
import facilities from '../assets/json/city_facility.json'
import occupations from '../assets/json/city_occupation.json'
import populations from '../assets/json/city_population.json'
import stations from '../assets/json/stations.json'
import lines from '../assets/json/lines.json'
import companies from '../assets/json/companies.json'
import lineStations from '../assets/json/line_stations.json'
import analysisData from '~/assets/json/analyzed_column_json/13.json'
interface State {
    cities: City
    addresses: Address,
    facilities: any,
    occupations: any,
    populations: any,
    stations: Station,
    lines: Line,
    lineStations: LineStations,
    companies: Company[],
    analysisData: any
}
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
    cities: cities,
    addresses: addresses,
    facilities: facilities,
    occupations: occupations,
    populations: populations,
    stations: stations,
    lines: lines,
    lineStations: lineStations,
    companies: companies,
    analysisData: analysisData
};

const getters = {
    cities: (state: State) => state.cities,
    addresses: (state: State) => state.addresses,
    facilities: (state: State) => state.facilities,
    occupations: (state: State) => state.occupations,
    populations: (state: State) => state.populations,
    stations: (state: State) => state.stations,
    lines: (state: State) => state.populations,
    lineStations: (state: State) => state.lineStations,
    companies: (state: State) => state.companies,
    analysisData: (state: State) => state.analysisData,
    combineStationsWithLines: (state: State, getters: any) => {
        return getters.stations.map((station: Station) => {
            const lineIds = getters.lineStations.filter((lineStation: LineStations) => lineStation.station_id == station.id).map((lineStation: LineStations) => lineStation.line_id)
            const lines = getters.lines.filter((line: Line) => lineIds.includes(line.id))
            station['lines'] = lines;
            return station;
        })
    },
    combineCompaniesWithStations: (state: State, getters: any) => {
        return getters.companies.map((station: Station) => {
            const lineIds = getters.lineStations.filter((lineStation: LineStations) => lineStation.station_id == station.id).map((lineStation: LineStations) => lineStation.line_id)
            const lines = getters.lines.filter((line: Line) => lineIds.includes(line.id))
            station['lines'] = lines;
            return station;
        })
    },
}

const mutations = {

};

const actions = {

};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
