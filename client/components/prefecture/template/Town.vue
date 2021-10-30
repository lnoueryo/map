<template>
  <div>
    <div v-for="(town, i) in towns" :key="i">
      <div class="d-flex align-center text-center py-4" v-if="i % 6 == 0 && !tablet">
        <div class="town-name" @click="type = '町名'">
          町名<br>
          <v-btn icon @click.stop="highLowSwitch = !highLowSwitch;type = '町名';sortValue = ''">
            <v-icon small :style="!highLowSwitch && type == '町名' ? {transform: 'rotate(0deg)'} : {transform: 'rotate(180deg)'}">mdi-menu-down</v-icon>
          </v-btn>
        </div>
        <div class="columns">
          <div class="d-flex align-center justify-space-between pa-1">
            <div class="property pa-2">種類<br><div>　　</div></div>
            <div class="column pa-2" :class="{'active' : sortValue == columnItem.value}" v-for="(columnItem, k) in columnItems" :key="k" @click.stop="sortColumns(columnItem.value)">
              <div>
                {{columnItem.title}}<br>
                <v-btn icon @click.stop="sortColumns(columnItem.value, !highLowSwitch)">
                  <v-icon small :style="!highLowSwitch && sortValue == columnItem.value ? {transform: 'rotate(0deg)'} : {transform: 'rotate(180deg)'}">mdi-menu-down</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="table-row text-center py-2">
        <div class="town-name">
          <div>{{town.name}}</div>
          <div>{{roundPercentage(town.count_ratio)}}%</div>
        </div>
        <div class="columns">
          <div class="table-data pa-1" v-if="tablet">
            <div>種類</div>
            <div class="column" v-for="(columnItem, k) in columnItems" :key="k">
              <div>{{columnItem.title}}</div>
            </div>
          </div>
          <div class="table-data pa-1" v-for="(column, j) in town.columns" :key="j">
            <div class="property" @click="changeType(column.property)">{{column.property}}</div>
            <div class="column" v-for="(columnItem, k) in columnItems" :key="k">
              <div>{{column.property == '家賃' ? roundPrice(column[columnItem.value]) : round(column[columnItem.value])}} <span v-if="column.property == '家賃'">万</span>{{units[j]}}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: ['analysisData'],
  data() {
    return {
      type: '家賃',
      sortValue: 'mean',
      highLowSwitch: true,
    }
  },
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
    towns() {
      const townsCopy = JSON.parse(JSON.stringify(this.analysisData.towns));
      if(this.type == '町名') {
        return townsCopy.sort((a, b) => {
          const c = a?.count ?? -1;
          const d = b?.count ?? -1;
          if(this.highLowSwitch) return c < d ? 1 : -1;
          else return c > d ? 1 : -1;
        })
      }
      return townsCopy.sort((a, b) => {
        if(this.highLowSwitch) return (a.columns[0] ? a.columns.find((column) => column.property == this.type)[this.sortValue] : -1) < (b.columns[0] ? b.columns.find((column) => column.property == this.type)[this.sortValue] : -1) ? 1 : -1;
        else return (a.columns[0] ? a.columns.find((column) => column.property == this.type)[this.sortValue] : -1) > (b.columns[0] ? b.columns.find((column) => column.property == this.type)[this.sortValue] : -1) ? 1 : -1;
      });
    }
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
    sortColumns(sortValue, highLowSwitch = true) {
      if(this.type == '町名') this.type = '家賃'
      this.sortValue = sortValue;
      this.highLowSwitch = highLowSwitch;
    },
    changeType(type) {
      if(this.type == '町名') this.sortValue = 'mean'
      this.type = type;
    }
  }
}
</script>

<style lang="scss" scoped>
  .active {
    background-color: #53535371;
  }
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
    // padding: 4px 16px;
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