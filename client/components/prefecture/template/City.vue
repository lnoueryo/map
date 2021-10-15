<template>
  <div>
    <div class="d-flex align-center text-center py-4" v-if="!tablet">
      <div class="town-name"></div>
      <div class="columns pa-4">
        <div class="d-flex align-center justify-space-between">
          <div class="property">種類</div>
          <div class="column" v-for="(columnItem, k) in columnItems" :key="k">
            <div>{{columnItem.title}}</div>
          </div>
        </div>
      </div>
    </div>
    <div class="table-row text-center py-4">
      <div class="town-name">{{analysisData.name}}</div>
      <div class="columns">
        <div class="table-data py-1" v-if="tablet">
          <div>種類</div>
          <div class="column" v-for="(columnItem, k) in columnItems" :key="k">
            <div>{{columnItem.title}}</div>
          </div>
        </div>
        <div class="table-data py-1" v-for="(column, j) in analysisData.columns" :key="j">
          <div class="property">{{column.property}}</div>
          <div class="column" v-for="(columnItem, k) in columnItems" :key="k">
            <div>{{column.property == '家賃' ? roundPrice(column[columnItem.value]) : round(column[columnItem.value])}} <span v-if="column.property == '家賃'">万</span>{{units[j]}}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['analysisData'],
  computed: {
    columnItems() {
      return [
        {title: '平均', value: 'mean'},
        {title: '中央値', value: '50%'},
        {title: '標準偏差', value: 'std'},
        {title: '最小値', value: 'min'},
        {title: '最大値', value: 'max'}
      ]
    },
    units(){
      return ['円', '年', '㎡']
    },
    smp() {
      return this.$store.getters.windowSize.x < 500
    },
    tablet() {
      return this.$store.getters.windowSize.x < 768
    },
  },
  methods: {
    round(num) {
      return Math.round(num*100) / 100
    },
    roundPrice(num) {
      return Math.round(num / 100) / 100;
    },
    roundPercentage(num) {
      return Math.round(num*10000) / 100
    },
  }
}
</script>

<style lang="scss" scoped>
  .table-row {
    display: flex;
    align-items: center;
  }
  .town-name {
    width: 15%;
  }
  .columns {
    width: 85%;
  }
  .table-data {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 16px;
  }
  .property {
    width: 15%;
  }
  .column {
    width: 12.25%;
  }
  @media screen and (max-width: 768px) {
    .table-row {
      display: block;
    }
    .town-name {
      width: 100%;
    }
    .columns {
      width: 100%;
      display: flex;
      justify-content: space-around;
    }
    .table-data {
      display: block;
      width: 25%;
      padding: 4px;
    }
    .property {
      width: 100%;
      display: flex;
      justify-content: center;
    }
    .column {
      width: 100%;
      max-height: 24px;
      overflow: hidden;
    }
  }
</style>