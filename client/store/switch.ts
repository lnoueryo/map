
interface State {
    fields: string[],
    changeList: number,
    markerSwitch: boolean,
    lineSwitch: boolean,
    chartSwitch: boolean,
    dotSwitch: boolean,
    stationSwitch: boolean,
    citySwitch: boolean,
    spotSwitch: boolean,
    markerSwitches: {[key: string]: boolean}
}

const state = {
    fields: ['stations', 'cities', 'spots'],
    changeList: 0,
    markerSwitch: true,
    lineSwitch: true,
    chartSwitch: false,
    dotSwitch: true,
    markerSwitches: {}
};

const getters = {
    fields: (state: State) => state.fields,
    changeList: (state: State): number => state.changeList,
    markerSwitches: (state: State) => state.markerSwitches,
    markerSwitch: (state: State): boolean => state.markerSwitch, //マーカー表示のboolean
    lineSwitch: (state: State) => state.lineSwitch, //路線図表示のboolean
    chartSwitch: (state: State) => state.chartSwitch, //グラフ表示のboolean
    dotSwitch: (state: State) => state.dotSwitch, //ドット表示のboolean
}

const mutations = {
    changeList: (state: State, payload: number) => {
        state.changeList = payload;
    },
    makeSwitches: (state: State) => {
        state.fields.forEach((field: string) => {
            state.markerSwitches[field] = true
        });
    },
    markerSwitch: (state: State, payload: boolean) => {
        state.markerSwitch = payload;
    },
    lineSwitch: (state: State, payload: boolean) => {
        state.lineSwitch = payload;
    },
    chartSwitch: (state: State, payload: boolean) => {
        state.chartSwitch = payload;
    },
    stationSwitch: (state: State, payload: boolean) => {
        state.stationSwitch = payload;
    },
    changeMarkerSwitches: (state: State, payload: {category: string, status: boolean}) => {
        let obj: {[key: string]: boolean} = {}
        obj[payload.category] = payload.status
        state.markerSwitches = Object.assign({}, state.markerSwitches, obj)
    },
    dotSwitch: (state: State, payload: boolean) => {
        state.dotSwitch = payload;
    },
};

const actions = {
    changeList: (context: any, payload: number) => {
        context.commit('changeList', payload)
    },
    changeMarkerSwitch: (context: any, payload: boolean) => {
        context.commit('markerSwitch', payload)
    },
    changeLineSwitch: (context: any, payload: boolean) => {
        context.commit('lineSwitch', payload)
    },
    changeChartSwitch: (context: any, payload: boolean) => {
        context.commit('chartSwitch', payload)
    },
    changeMarkerSwitches: (context: any, payload: {category: string, status: boolean}) => {
        context.commit('changeMarkerSwitches', payload)
    },
    changeDotSwitch: (context: any, payload: boolean) => {
        context.commit('dotSwitch', payload)
    },
    makeSwitches: (context: any) => {
        context.commit('makeSwitches')
    }
};

export default {
    namespace: true,
    state,
    getters,
    mutations,
    actions,
}
