<template>
  <div>
    <nav
      class="bottom-bar"
      :style="
        position
          ? { top: show ? '0' : '100vh', overflowY: 'scroll' }
          : { top: show ? `${vh(85)}` : '100vh', overflowY: 'initial' }
      "
    >
      <div class="hidden-frame">
        <div class="d-flex" v-if="show">
          <div class="mx-2 w100">
            <v-btn block @click="upWiki" v-if="!position">up</v-btn>
            <v-btn block @click="downWiki" v-else>down</v-btn>
          </div>
          <div class="mx-2 w100">
            <v-btn block @click="fade">delete</v-btn>
          </div>
        </div>
        <div ref="component" :style="componentStyle">
          <slot></slot>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
export default {
  props: ["show", "difference"],
  data() {
    return {
      translateY: 0,
      navStyle: {
        height: 0,
        transform: "",
        transition: "all .5s",
        zIndex: 0,
      },
      componentStyle: {
        height: "initial",
        transition: "all .5s",
        overflowY: "hidden",
        overflowX: "hidden",
      },
      position: false,
      component: this.$refs.component,
    };
  },
  computed: {
    transform() {
      return {
        transform: `translateY(${this.translateY}px)`,
        transition: "all .5s",
      };
    },
  },
  watch: {
    // show: {
    //     handler(v) {
    //         if (v) {
    //             // const newNavStyle = {height: '100px', transform: 'translateY(-100px)'};
    //             // const newComponentStyle = {height: '40px'};
    //             // this.navStyle = {...this.navStyle, ...newNavStyle};
    //             // this.componentStyle = {...this.componentStyle};
    //         }
    //     }
    // }
  },
  methods: {
    upWiki() {
      this.position = true;
      // const newNavStyle = {height: `calc(100vh - ${this.difference})`, transform: `translateY(calc(-100vh + ${this.difference}))`, zIndex: 10};
      // const newComponentStyle = {height: 'calc(100vh - 205px)', 'overflowX': 'hidden', 'overflowY': 'scroll'};
      // this.navStyle = {...this.navStyle, ...newNavStyle};
      // this.componentStyle = {...this.componentStyle, ...newComponentStyle};
    },
    downWiki() {
      this.$refs.component.scrollTop = 0;
      this.position = false;
      // const newNavStyle = {height: '100px', transform: 'translateY(-100px)', zIndex: 0};
      // const newComponentStyle = {overflowY: 'hidden'};
      // this.navStyle = {...this.navStyle, ...newNavStyle};
      // this.componentStyle = {...this.componentStyle, ...newComponentStyle};
    },
    fade() {
      this.$refs.component.scrollTop = 0;
      this.position = false;
      this.$emit("hide");
      // this.show = false;
      // const newNavStyle = {height: '0px', transform: 'translateY(0px)', zIndex: 0};
      // const newComponentStyle = {overflowY: 'hidden'};
      // this.navStyle = {...this.navStyle, ...newNavStyle};
      // this.componentStyle = {...this.componentStyle, ...newComponentStyle};
    },
    vh(vh) {
      return window.innerHeight * 0.01 * vh + "px";
    },
  },
};
</script>

<style lang="scss" scoped>
.bottom-bar {
  position: absolute;
  right: 0;
  left: 0;
  top: 100vh;
  z-index: 2;
  color: black;
  background-color: #ffffff;
  transition: all 0.5s;
  bottom: 0;
}
.mw-parser-output {
  position: relative;
  z-index: 10;
  background-color: white;
  margin: auto;
}
.hidden-frame {
  width: 100%;
}
.w100 {
  width: 100%;
}
@media screen and (max-width: 500px) {
  .bottom-bar {
    position: fixed;
    z-index: 5;
  }
}
</style>