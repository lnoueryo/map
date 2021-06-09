import { NuxtApp } from '@nuxt/types/app'
import { NuxtAxiosInstance } from '@nuxtjs/axios';
let $axios: NuxtAxiosInstance;
let $nuxt: NuxtApp
export function initializeAxios(axiosInstance: NuxtAxiosInstance): void {
  $axios = axiosInstance;
}
import Vue from 'vue'
Vue.config.errorHandler = (err, vm) => {
  const $nuxt = vm.$root as NuxtApp
  $nuxt.error(err)
}

export { $axios, $nuxt };
