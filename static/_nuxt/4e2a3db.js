(window.webpackJsonp=window.webpackJsonp||[]).push([[36],{517:function(e,t,r){var content=r(624);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,r(22).default)("12dbb53c",content,!0,{sourceMap:!1})},623:function(e,t,r){"use strict";r(517)},624:function(e,t,r){var n=r(21)(!1);n.push([e.i,'.map-container[data-v-10c208eb]{position:relative;width:100%;height:100vh;max-height:calc(100vh - 64px)}.map-container .line-chart[data-v-10c208eb]{position:absolute;top:40px;bottom:0;right:0;left:0;margin:auto}.map-container .map-top[data-v-10c208eb]{position:absolute;z-index:1}.map-container .dot[data-v-10c208eb]{position:absolute;top:0;bottom:0;left:0;right:0;margin:auto;width:9px;height:9px;border-radius:50%;background-color:red;opacity:.4;transition:all 2s}.map-container #map[data-v-10c208eb]{width:100%;height:100%;position:relative;transition:all .5s}.map-container .show-line[data-v-10c208eb]{opacity:.4}.map-container #overview-wrapper[data-v-10c208eb]{position:absolute;width:30%;bottom:50px;left:15px;box-shadow:0 2px 6px rgba(0,0,0,.7)}.map-container #overview-wrapper #overview-container[data-v-10c208eb]{position:relative;width:100%}.map-container #overview-wrapper #overview-container #overview[data-v-10c208eb]{position:absolute;top:0;left:0;width:100%;height:100%}.map-container #overview-wrapper #overview-container[data-v-10c208eb]:before{content:"";display:block;padding-top:56.25%}@media screen and (max-width:500px){.map-container .map-container[data-v-10c208eb]{max-height:calc(100vh - 120px)}}',""]),e.exports=n},686:function(e,t,r){"use strict";r.r(t);r(6),r(8),r(14),r(15);var n=r(5),o=r(2),c=(r(40),r(17),r(33),r(36),r(7),r(56),r(67),r(28),r(99),r(10),r(41),r(0)),f=r(98);function m(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);e&&(r=r.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,r)}return t}function h(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?m(Object(source),!0).forEach((function(t){Object(o.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):m(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var l=c.a.extend({components:{MapTop:function(){return r.e(31).then(r.bind(null,694))}},data:function(){return{markers:{},polygons:[],timer:null}},computed:h(h({},Object(f.b)("home",["fields","prefectures","selectedMarker","selectedCityItems"])),Object(f.b)("switch",["markerSwitches","markerSwitch","lineSwitch","chartSwitch","dotSwitch"])),watch:{$route:function(e,t){if("click"in e.query){var r=sessionStorage.getItem("tokyo-map");this.$mapConfig.focusMarker(JSON.parse(r),11)}this.checkQuery()}},beforeCreate:function(){this.$store.dispatch("switch/makeSwitches")},created:function(){var e=this;this.fields.forEach((function(t){e.markers[t]=[]}))},mounted:function(){var e=this;return Object(n.a)(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,e.setMap();case 2:e.checkQuery(),e.$mapConfig.map.addListener("bounds_changed",(function(){var t=e.$mapConfig.currentBounds(),n=e.$mapConfig.map.getCenter(),o={lat:n.lat(),lng:n.lng()},c=e.$mapConfig.map.getZoom();null!==r&&clearTimeout(r),r=setTimeout((function(){e.$store.dispatch("home/getCity",{mapCenter:o,zoom:c}),e.$store.dispatch("home/getCurrentBounds",t)}),1e3)}));case 4:case"end":return t.stop()}}),t)})))()},methods:{setMap:function(){var e=this;return Object(n.a)(regeneratorRuntime.mark((function t(){var r,n;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:r=e.$refs.map,n={zoom:8,restriction:{latLngBounds:{north:37.360687,south:34.030351,west:137.9403931,east:140.9368243},strictBounds:!1}},e.$mapConfig.mapOptions(n),e.$mapConfig.makeMap(r),e.$mapConfig.placesService();case 6:case"end":return t.stop()}}),t)})))()},prefectureMarkerFunction:function(marker,e){var t=this;marker.addListener("click",function(){var r=Object(n.a)(regeneratorRuntime.mark((function r(n){return regeneratorRuntime.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:t.$router.push("/?prefecture_id=".concat(e.id));case 1:case"end":return r.stop()}}),r)})));return function(e){return r.apply(this,arguments)}}())},cityMarkerFunction:function(marker,e){var t=this;marker.addListener("click",function(){var r=Object(n.a)(regeneratorRuntime.mark((function r(n){return regeneratorRuntime.wrap((function(r){for(;;)switch(r.prev=r.next){case 0:t.$router.push("/?prefecture_id=".concat(t.$route.query.prefecture_id,"&city_code=").concat(e.city_code));case 1:case"end":return r.stop()}}),r)})));return function(e){return r.apply(this,arguments)}}())},spotMarkerFunction:function(marker,e){var t=this;marker.addListener("click",(function(r){t.$store.dispatch("info/spotDetail",e)}))},checkQuery:function(){var e=this.$route.query;(null==e?void 0:e.prefecture_id)&&e.city_code?this.selectCityMarker(e):(null==e?void 0:e.prefecture_id)?this.setCityMarkers(e.prefecture_id):this.setPrefectureMarkers()},setPrefectureMarkers:function(){var e=this;return Object(n.a)(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){for(;;)switch(t.prev=t.next){case 0:return e.$mapConfig.resetAllMarkers(e.markers),t.next=3,e.$mapConfig.makeMarkers([{prefectures:e.prefectures}],"prefectures",e.prefectureMarkerFunction);case 3:e.markers.prefectures=t.sent,r={zoom:10},e.$mapConfig.mapOptions(r);case 6:case"end":return t.stop()}}),t)})))()},setCityMarkers:function(e){this.$mapConfig.resetAllMarkers(this.markers);var t=this.prefectures.find((function(t){return t.id==e}));if(this.markers.cities=this.$mapConfig.makeMarkers([t],"cities",this.cityMarkerFunction),!("click"in this.$route.query)){this.$mapConfig.focusMarker(t,11)}},selectCityMarker:function(e){this.$mapConfig.resetAllMarkers(this.markers);var t=this.prefectures.reduce((function(a,b){return a.cities.concat(b.cities)})).cities.find((function(t){return t.city_code==e.city_code}));this.markers.spots=this.$mapConfig.makeMarkers([t],"spots",this.spotMarkerFunction);this.$mapConfig.focusMarker(t,14)},clearTime:function(){this.timer&&clearTimeout(this.timer)},onClickMap:function(e){var t=this;return Object(n.a)(regeneratorRuntime.mark((function e(){return regeneratorRuntime.wrap((function(e){for(;;)switch(e.prev=e.next){case 0:t.$mapConfig.map.addListener("dblclick",(function(e){var r=JSON.stringify({lat:e.latLng.lat(),lng:e.latLng.lng()});sessionStorage.setItem("tokyo-map",r);var n=Object.assign({click:null},t.$route.query);delete n[Object.keys(t.$route.query).slice(-1)[0]],t.$router.push({query:n})}));case 1:case"end":return e.stop()}}),e)})))()}}}),d=(r(623),r(74)),component=Object(d.a)(l,(function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{staticClass:"map-container"},[r("map-top",{staticClass:"map-top"}),e._v(" "),r("div",{ref:"map",class:{"show-line":e.chartSwitch},attrs:{id:"map"}}),e._v(" "),e.dotSwitch?r("div",{staticClass:"dot"}):e._e()],1)}),[],!1,null,"10c208eb",null);t.default=component.exports}}]);