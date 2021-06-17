<template>
    <div>
        <div class="toggle-switch">
            <div class="mr-3"><slot></slot></div>
            <input :id="id" class="toggle-input" type='checkbox' v-model="checked"/>
            <label :for="id" :style="value?{backgroundColor: backgroundColor}:{backgroundColor: '#ccc'}" class="toggle-label"/>
            <span></span>
        </div>
    </div>
</template>

<script>
export default {
  props:['id', 'backgroundColor', 'value'],
    computed:{
      checked:{
        get(){
          return this.value;
        },
        set(newValue) {
          this.$emit("input", newValue);
        },
      }
    }
}
</script>

<style lang="scss" scoped>
input {
  position: relative;
  width: 100%;
  height: 100%;
  z-index: 5;
  opacity: 0;
  cursor: pointer;
  display: none;
}

label {
  cursor: pointer;
  width: 38px;
  height: 20px;
  background: #ccc;
  position: relative;
  display: inline-block;
  border-radius: 46px;
  transition: 0.4s;
  box-sizing: border-box;
  &:after {
    content: '';
    position: absolute;
    width: 20px;
    height: 20px;
    border-radius: 100%;
    left: 0;
    top: 0;
    z-index: 2;
    background: #fff;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.2);
    transition: 0.4s;
  }
}

input:checked {
  +label{
    background-color: #4BD865;
    &:after{
      left: 19px;
    }
  }
}

p {
  margin-top: 50px;
  text-align: center;
  font-weight: bold;
}

.toggle-switch {
  position: relative;
  display:flex;
  align-items:flex-end;
}
</style>