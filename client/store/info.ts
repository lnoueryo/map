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
        try {
            const response = await $axios.$get('/api/map/twitter/', { params: payload });
            context.commit('twitterInfo', response)
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection')
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    getEvents: async (context: any) => {
        try {
            const response = await $axios.$get('/api/map/event/');
            context.commit('events', response);
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    getAroundSpot: async (context: any, payload: Spot) => {
        try {
            const response = await $axios.$get('/api/map/search-by-place-info/', {params: payload});
            context.commit('aroundSpot', response);

        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    getAroundStationInfo: async (context: any, payload: Spot) => {
        try {
            const response = await $axios.$get('/api/map/search-by-place-info/', {params: payload});
            context.commit('aroundStationInfo', response);
        } catch (err: any) {
            if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
            else context.dispatch('errorDialog', true, { root: true })
        }
    },
    spotDetail: async (context: any, payload: Spot) => {
        if (payload) {
            try {
                const result = await $nuxt.$mapConfig.placesDetail(payload.place_id);
                context.commit('spotDetail', result);
            } catch (err: any) {
                if(!err?.response || err?.response.status == 504) $nuxt.$router.push('/bad-connection');
                else context.dispatch('errorDialog', true, { root: true });
            }
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
