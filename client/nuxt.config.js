import colors from 'vuetify/es5/util/colors'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,
  router: {
    base: ''
   },
  // Target: https://go.nuxtjs.dev/config-target
  target: 'static',

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    base: {
      href: 'router.base'
    },
    titleTemplate: '%s - map',
    title: 'map',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/logo.png' },
      // { rel: 'stylesheet', integrity: 'sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A==', href: 'https://unpkg.com/leaflet@1.7.1/dist/leaflet.css', crossorigin: '' },
    ],
    script: [
      { src: `https://maps.googleapis.com/maps/api/js?key=${process.env.NODE_ENV === 'production' ? process.env.PROD_API_KEY : process.env.DEV_API_KEY}&libraries=geometry,places&v=quarterly`, defer: true, body: true },
      { src: 'https://polyfill.io/v3/polyfill.min.js?features=default', defer: true, body: true },
      // { src: 'https://unpkg.com/@googlemaps/markerclustererplus/dist/index.min.js', defer: true, body: true },
      // { src: 'https://unpkg.com/leaflet@1.7.1/dist/leaflet-src.js', integrity: 'sha512-I5Hd7FcJ9rZkH7uD01G3AjsuzFy3gqz7HIJvzFZGFt2mrCS4Piw9bYZvCgUE0aiJuiZFYIJIwpbNnDIM6ohTrg==', crossorigin: '', defer: true, body: true },
      // { src: 'https://unpkg.com/leaflet.gridlayer.googlemutant@latest/dist/Leaflet.GoogleMutant.js', defer: true, body: true },
    ]
  },
  publicRuntimeConfig: {
    environment: process.env.environment
  },
  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/axios-accessor',
    '~/plugins/map',
    '~/plugins/component'
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://go.nuxtjs.dev/pwa
    '@nuxtjs/pwa',
    '@nuxtjs/proxy',
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  // sakura本番
  // axios: {
  //   baseURL: 'https://map-ai7ganlifq-an.a.run.app',
  //   retry: { retries: 5 },
  // },
  // cloudrun本番
  // axios: {
  //   baseURL: '/',
  //   retry: { retries: 5 },
  // },

  //ローカル
  axios: {
    baseURL: process.env.NODE_ENV === 'production' ? process.env.baseURL : 'http://localhost:3000/api/',
  },
  proxy: {
    '/api': {
      target: "http://localhost:8000/",
      pathRewrite: {
        '^/api': ''
      }
    },
  },

  // PWA module configuration: https://go.nuxtjs.dev/pwa
  pwa: {
    manifest: {
      lang: 'en',
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      }
    }
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    publicPath: '/static/_nuxt/',
    terser: {
      terserOptions: {
        compress: { drop_console: true }
      },
    },
  },
  generate: {
    dir: './dist'
  },
}
