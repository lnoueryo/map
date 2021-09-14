import { $axios } from '~/utils/api';

interface State {
    stationInfo: null | string,
    cityWikiInfo: null | string,
    twitterInfo: Twitter[],
    events: string[],
    searching: boolean,
    spotDetail: null | google.maps.places.PlaceResult
}
interface Twitter { id: number, 'name': string, 'profile_image_url': string, 'followers_count': number, 'friends_count': number, 'text': string, 'images': string[] }
interface Spot { name: string, place_id: string, address: string, lat: string, lng: string }
const state = {
    stationInfo: null,
    cityWikiInfo: null,
    twitterInfo: [],
    searching: false,
    events: [],
    spotDetail: null
};

const getters = {
    events: (state: State) => state.events,
    stationInfo: (state: State) => state.stationInfo, //ウィキから引っ張ってきたhtmlを返す
    cityWikiInfo: (state: State) => state.cityWikiInfo, //ウィキから引っ張ってきたhtmlを返す
    twitterInfo: (state: State) => state.twitterInfo, //ツイッターから引っ張ってきたjsonを返す
    searching: (state: State) => state.searching, //ウィキ検索中のloading処理
    spotDetail: (state: State) => state.spotDetail,
}

const mutations = {
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
    events: (state: State, payload: string[]) => {
        state.events = payload;
    },
    spotDetail: (state: State, payload: google.maps.places.PlaceResult) => {
        state.spotDetail = payload;
    }
};

const actions = {
    getStationInfo: async (context: any, payload: string) => {
        context.commit('searching', true)
        let err, response = await $axios.$get('/api/wiki/', { params: payload });
        if (err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('stationInfo', response)
    },
    getTwitterInfo: async (context: any, payload: string) => {
        console.log(payload)
        let err, response = await $axios.$get('/api/twitter/', { params: payload });
        if (err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        console.log(response)
        context.commit('twitterInfo', response)
    },
    getCityWikiInfo: async (context: any, payload: string) => {
        if (payload) {
            let err, response = await $axios.$get('/api/wiki/', { params: payload });
            if (err) {
                console.log(err)
                context.commit('cityWikiInfo', 'ページが見つかりませんでした')
            }
            context.commit('cityWikiInfo', response);
        } else context.commit('cityWikiInfo', payload);
    },
    getEvents: async (context: any) => {
        const response = await $axios.$get('/api/event/');
        context.commit('events', response);
    },
    spotDetail: async (context: any, payload: Spot) => {
        if (payload) {
            const result = await $nuxt.$mapConfig.placesDetail(payload.place_id);
            context.commit('spotDetail', result);
        } else context.commit('spotDetail', payload);
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
