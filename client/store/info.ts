import { $axios } from '~/utils/api';

interface State {
    stationInfo: null | string,
    twitterInfo: Twitter[],
    events: string[],
    aroundSpot: string[],
    aroundStationInfo: string[],
    searching: boolean,
    spotDetail: null | google.maps.places.PlaceResult
}
interface Twitter { id: number, 'name': string, 'profile_image_url': string, 'followers_count': number, 'friends_count': number, 'text': string, 'images': string[] }
interface Spot { name: string, place_id: string, address: string, lat: string, lng: string }
const state = {
    stationInfo: null,
    twitterInfo: [],
    searching: false,
    events: [],
    spotDetail: null,
    aroundSpot: [],
    aroundStationInfo: [],
};

const getters = {
    events: (state: State) => state.events,
    aroundSpot: (state: State) => state.aroundSpot,
    aroundStationInfo: (state: State) => state.aroundStationInfo,
    stationInfo: (state: State) => state.stationInfo, //ウィキから引っ張ってきたhtmlを返す
    twitterInfo: (state: State) => state.twitterInfo, //ツイッターから引っ張ってきたjsonを返す
    searching: (state: State) => state.searching, //ウィキ検索中のloading処理
    spotDetail: (state: State) => state.spotDetail,
}

const mutations = {
    stationInfo: (state: State, payload: string) => {
        state.stationInfo = payload;
    },
    twitterInfo: (state: State, payload: Twitter[]) => {
        state.twitterInfo = payload;
    },
    searching: (state: State, payload: boolean) => {
        state.searching = payload;
    },
    events: (state: State, payload: string[]) => {
        state.events = payload;
    },
    aroundSpot: (state: State, payload: string[]) => {
        state.aroundSpot = payload;
    },
    aroundStationInfo: (state: State, payload: string[]) => {
        state.aroundStationInfo = payload;
    },
    spotDetail: (state: State, payload: google.maps.places.PlaceResult) => {
        state.spotDetail = payload;
    }
};

const actions = {
    getTwitterInfo: async (context: any, payload: string) => {
        let err, response = await $axios.$get('/api/twitter/', { params: payload });
        if (err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('twitterInfo', response)
    },
    getEvents: async (context: any) => {
        const response = await $axios.$get('/api/event/');
        context.commit('events', response);
    },
    getAroundSpot: async (context: any, payload: Spot) => {
        const response = await $axios.$get('/api/search-by-place-info/', {params: payload});
        context.commit('aroundSpot', response);
    },
    getAroundStationInfo: async (context: any, payload: Spot) => {
        const response = await $axios.$get('/api/search-by-place-info/', {params: payload});
        context.commit('aroundStationInfo', response);
    },
    spotDetail: async (context: any, payload: Spot) => {
        if (payload) {
            const result = await $nuxt.$mapConfig.placesDetail(payload.place_id);
            context.commit('spotDetail', result);
        } else context.commit('spotDetail', payload);
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
