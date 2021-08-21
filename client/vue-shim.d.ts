
declare module '*.vue' {
    import type Vue from 'vue'
    export default Vue
  }
declare module "*.json" {
    const value: any;
    export default value;
}
declare module "*.csv" {
    const value: any;
    export default value;
}
declare module "*.ts" {
    const value: any;
    export default value;
}
declare module '*.vue' {
    import { MapConfig } from '~/plugins/map';
  
    module 'vue/types/vue' {
      interface Vue {
        $mapConfig: MapConfig;
      }
    }
  }