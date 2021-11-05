<template>
  <div class="w100 search-box">
    <div class="cp_iptxt" @click="focus" @mouseover="blur = false">
      <div class="d-flex">
        <input
          ref="input"
          type="text"
          :placeholder="placeholder"
          @blur="check"
          @keyup.enter="onEnter"
          @input="input($event)"
        />
        <v-icon class="close" @click="searchWord = null">mdi-close</v-icon>
      </div>
      <v-icon id="magnify">mdi-magnify</v-icon>
    </div>
    <div class="w100" @mouseenter="blur = true" @mouseleave="blur = false">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: ["value", "placeholder", "backgroundColor"],
  data() {
    return {
      blur: false,
    };
  },
  methods: {
    focus() {
      this.$refs.input.focus();
    },
    check() {
      if (this.blur) {
        try {
					this.$refs.input.focus();
				} catch (error) {
					
				}
      }
    },
    onEnter() {
      this.$emit("select");
    },
    input(word) {
      this.$emit('searchWord', word.target.value);
    }
  },
};
</script>

<style lang="scss" scoped>
.cp_iptxt {
  position: relative;
  input[type="text"] {
    font: 15px/24px sans-serif;
    box-sizing: border-box;
    width: 100%;
    padding: 0.3em;
    transition: 0.5s;
    border: 1px solid #1b2538;
    border-radius: 4px;
    outline: none;
  }
  input[type="text"]:focus {
    border-color: #da3c41;
    transition: 0.5s;
  }
  input[type="text"] {
    padding-left: 40px;
  }
  i {
    position: absolute;
    top: 0px;
    bottom: 0px;
    left: 0;
    padding: 0px 8px;
    transition: 0.5s;
    color: #aaaaaa;
  }
  input[type="text"]:focus + i {
    color: #da3c41;
  }
  .close {
    position: absolute;
    top: 0;
    bottom: 0;
    right: 5px;
    left: initial;
    color: #aaaaaa;
  }
}
.w100 {
  width: 100%;
}
.menu {
  position: absolute;
  height: 0;
  visibility: hidden;
  opacity: 0;
  width: 100%;
  transform: translateY(-25px) rotateX(30deg);
  transition: all 0.2s;
  transition-timing-function: ease-in;
  border-radius: 5px;
}
.search-box {
  position: relative;
}

.search-box:focus-within {
  .menu {
    visibility: visible;
    opacity: 1;
    height: auto;
    transform: translateY(0) rotateX(0deg);
    transition: all 0.2s;
    transition-delay: 0.1s;
    transition-timing-function: ease-out;
    z-index: 3;
    box-shadow: 0 0 0 1px rgb(208, 208, 208);
  }
}
</style>