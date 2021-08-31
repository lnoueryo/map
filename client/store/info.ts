import { $axios } from '~/utils/api';

interface State {
    stationInfo: null|string,
    cityWikiInfo: null|string,
    twitterInfo: Twitter[],
    events: string[],
    searching: boolean
}
interface Twitter {id: number, 'name': string, 'profile_image_url': string, 'followers_count': number, 'friends_count': number, 'text': string, 'images': string[]}

const state = {
    stationInfo: null,
    cityWikiInfo: null,
    twitterInfo: [],
    searching: false,
    events: [],
};

const getters = {
    events: (state: State) => state.events,
    stationInfo: (state: State) => state.stationInfo, //ウィキから引っ張ってきたhtmlを返す
    cityWikiInfo: (state: State) => state.cityWikiInfo, //ウィキから引っ張ってきたhtmlを返す
    twitterInfo: (state: State) => state.twitterInfo, //ツイッターから引っ張ってきたjsonを返す
    searching: (state: State) => state.searching, //ウィキ検索中のloading処理
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
};

const actions = {
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
        context.commit('twitterInfo', response)
    },
    getCityWikiInfo: async(context: any, payload: string) => {
        let err, response = await $axios.$get('/api/wiki/', {params: payload});
        if(err) {
            console.log(err)
            context.commit('stationInfo', 'ページが見つかりませんでした')
        }
        context.commit('cityWikiInfo', response)
    },
    getEvents: async(context: any) => {
        const response = await $axios.$get('/api/event/');
        context.commit('events', response);
    },
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
