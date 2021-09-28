<template>
  <div>
    <div>
      <half-modal ref="wiki" :show="wikiReady" @hide="wikiReady = false">
        <wiki-info :wiki-data="cityWikiInfo"></wiki-info>
      </half-modal>
    </div>
  </div>
</template>


<script lang="ts">
interface Prefecture {
  id: string;
  name: string;
  wiki: string;
  lat: number;
  lng: number;
  cities: City[];
}
interface City {
  name: string;
  wiki: string;
  city_code: string;
  province: string;
  lat: string;
  lng: string;
  city: string;
  spots: Spot[];
}
interface Spot {
  id: number;
  name: string;
  place_id: string;
  address: string;
  lat: number;
  lng: number;
  prefecture_id: string;
  city_code: string;
  geohash: string;
}
interface DataType {
  prefecture: Prefecture | null;
  city: City | null;
  spot: Spot | null;
  wikiReady: boolean;
  placesReady: boolean;
  currentWikiData: string;
}
import Vue from "vue";
const HalfModal = () => import("../../global/HalfModal.vue");
const WikiInfo = () => import("../../global/WikiInfo.vue");
import { mapGetters } from "vuex";
export default Vue.extend({
  components: {
    HalfModal,
    WikiInfo,
  },
  data(): DataType {
    return {
      prefecture: null,
      city: null,
      spot: null,
      wikiReady: false,
      placesReady: false,
      currentWikiData: "",
      // abc: false
    };
  },
  computed: {
    ...mapGetters("station", ["prefectures", "cities", "spots"]),
    ...mapGetters("info", ["cityWikiInfo", "spotDetail"]),
    ...mapGetters("switch", ["changeLeftListSwitch"]),
  },
  watch: {
    prefecture(v) {
      const query = { ...this.$route.query, ...{ prefecture_id: v.id } };
      this.$router.push({ query: query });
    },
    city(v) {
      const query = { ...this.$route.query, ...{ city_code: v.city_code } };
      this.$router.push({ query: query });
    },
    spot(v) {
      if ((this as any).currentPlacesData == v.name) {
        (this as any).placesReady = true;
      } else {
        (this as any).currentPlacesData = v.name;
        this.$store.dispatch("info/spotDetail", v);
        this.$store.dispatch("info/getTwitterInfo", v);
        const wiki = this.$refs.wiki as any;
        wiki.fade();
      }
    },
    cityWikiInfo(v) {
      if (v) {
        (this as any).wikiReady = true;
      }
    },
    spotDetail(v) {
      if (v) {
        (this as any).placesReady = true;
      }
    },
  },
  methods: {
    getWiki(obj: City | Prefecture) {
      console.log(obj);
      if ((this as any).currentWikiData == obj.name) {
        (this as any).wikiReady = true;
      } else {
        (this as any).currentWikiData = obj.name;
        this.$store.dispatch("info/getCityWikiInfo", { name: obj.wiki });
        // const places = this.$refs.places as any;
        // places.fade()
      }
    },
  },
});
</script>

