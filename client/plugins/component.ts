import Vue from 'vue'

//componentsファイルにあるグローバルにしたいコンポーネントをimport
import ErrorDialog from '~/components/global/Error.vue'
//それを今回は'Button'というコンポーネント名で設定。
const ErrorConnectionDialog = () => import('~/components/global/Error.vue');
Vue.component('error', ErrorConnectionDialog)