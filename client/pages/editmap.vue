<template>
  <div class="d-flex" style="width: 100%">
    <div style="width: 360px">
      <toggle-switch
        key="1"
        class="mr-4"
        v-model="markerSwitch1"
        id="markerSwitch1"
        background-color="#ff9800"
        >マーカー</toggle-switch
      >
      <div>
        <item-select
          maxHeight="calc(100vh - 300px)"
          style="position: relative; z-index: 1"
          v-model="select"
          :items="$store.getters['editmap/lineStation']"
          placeholder="路線を選択"
          background-color="white"
          ripple="true"
        ></item-select>
      </div>
      <div class="d-flex">
        <toggle-switch
          key="3"
          class="mr-4"
          v-model="lineSwitch"
          id="line"
          background-color="#00E676"
          >路線</toggle-switch
        >
        <toggle-switch
          key="4"
          class="mr-4"
          v-model="stationSwitch"
          id="station"
          background-color="#ff9800"
          >駅</toggle-switch
        >
      </div>
      <text-box ref="textBox1" :map="map" :switch="markerSwitch1"></text-box>
    </div>
    <div class="map-container">
      <div id="map" ref="map"></div>
      <div
        style="
          position: absolute;
          top: 0;
          bottom: 0;
          right: 0;
          left: 0;
          z-index: 100;
        "
        v-if="loading"
      >
        <v-card
          color="primary"
          dark
          style="
            position: absolute;
            width: 250px;
            height: 60px;
            bottom: 0;
            top: 0;
            margin: auto;
            right: 0;
            left: 0;
          "
        >
          <v-card-text>
            Please stand by
            <v-progress-linear
              indeterminate
              color="white"
              class="mb-0"
            ></v-progress-linear>
          </v-card-text>
        </v-card>
      </div>
    </div>
    <div style="width: 360px">
      <toggle-switch
        key="1"
        class="mr-4"
        v-model="markerSwitch2"
        id="markerSwitch2"
        background-color="#ff9800"
        >マーカー</toggle-switch
      >
      <text-box ref="textBox2" :map="map" :switch="markerSwitch2"></text-box>
    </div>
  </div>
</template>

<script>
import TextBox from "../components/editmap/TextBox.vue";
import ToggleSwitch from "../components/global/ToggleSwitch.vue";
import ItemSelect from "~/components/global/ItemSelect.vue";
const kantoBounds = {
  north: 35.831409,
  south: 35.3111639,
  west: 138.9403931,
  east: 140.9762068,
};
export default {
  components: {
    TextBox,
    ToggleSwitch,
    ItemSelect,
  },
  data() {
    return {
      map: null,
      mapOptions: {
        center: new google.maps.LatLng(35.6729712, 139.7585771),
        restriction: { latLngBounds: kantoBounds, strictBounds: false },
        zoom: 14,
      },
      loading: false,
      value1: true,
      value2: false,
      line: true,
      station: false,
      selectedLineItem: [],
    };
  },
  computed: {
    markerSwitch1: {
      get() {
        return this.value1;
      },
      set(value) {
        google.maps.event.clearInstanceListeners(this.map);
        this.value1 = value;
        this.value2 = !this.value2;
      },
    },
    markerSwitch2: {
      get() {
        return this.value2;
      },
      set(value) {
        google.maps.event.clearInstanceListeners(this.map);
        this.value2 = value;
        this.value1 = !this.value1;
      },
    },
    lineSwitch: {
      get() {
        return this.line;
      },
      set(value) {
        this.line = value;
        this.station = !this.station;
      },
    },
    stationSwitch: {
      get() {
        return this.station;
      },
      set(value) {
        this.station = value;
        this.line = !this.line;
      },
    },
    select: {
      get() {
        if (Array.isArray(this.selectedLineItem)) {
          return this.selectedLineItem.length !== 0
            ? [this.selectedLineItem[0]]
            : [];
        }
        return [this.selectedLineItem];
      },
      set(value) {
        this.selectedLineItem = value[value.length - 1];
      },
    },
  },
  watch: {
    selectedLineItem(value) {
      if (value) {
        if (this.line) {
          this.$refs.textBox1.$refs.polyline.value = value.polygon;
        } else {
          const stations = value.stations.map((station) => {
            return { lat: station.lat, lng: station.lng };
          });
          this.$refs.textBox1.$refs.polyline.value = stations;
        }
        this.$refs.textBox1.onChangeText();
      }
    },
    line(value) {
      if (this.selectedLineItem && this.selectedLineItem.length !== 0) {
        console.log(this.selectedLineItem);
        if (this.line) {
          this.$refs.textBox1.$refs.polyline.value =
            this.selectedLineItem.polygon;
        } else {
          const stations = this.selectedLineItem.stations.map((station) => {
            return { lat: station.lat, lng: station.lng };
          });
          console.log(stations);
          this.$refs.textBox1.$refs.polyline.value = JSON.stringify(stations);
        }
        this.$refs.textBox1.onChangeText();
      }
    },
  },
  async created() {
    this.$store.dispatch("editmap/getLineStation");
  },
  mounted() {
    const mapEl = this.$refs.map;
    this.map = new google.maps.Map(mapEl, this.mapOptions);
  },
};
</script>

<style lang="scss" scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100vh;
  max-height: calc(100vh - 64px);
  #map {
    width: 100%;
    height: 100%;
    position: relative;
    padding-top: 56.25%;
  }
}
</style>