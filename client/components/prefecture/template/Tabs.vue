<template>
  <div>
    <div class="d-flex flex-wrap text-center" style="min-height: 322px">
      <div class="d-flex pa-4 align-center" v-for="(tabItem, i) in tabItems" :key="i">
        <div>
          <div class="py-1">
            {{tabItem.title}}
          </div>
          <div class="py-1">
            {{tabValues[tabItem.value]}}
            <span>{{unit}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['tabItems', 'tabValues', 'unit']
}
</script>
