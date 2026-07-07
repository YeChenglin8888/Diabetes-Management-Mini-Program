<template>
  <view class="chart-card">
    <canvas
      v-if="hasData"
      class="chart-canvas"
      :canvas-id="canvasId"
      :id="canvasId"
      @touchstart="touchChart"
    />
    <EmptyState v-else icon="~" title="暂无趋势" desc="记录几次后，这里会出现你的变化曲线。" />
  </view>
</template>

<script setup>
import { computed, getCurrentInstance, nextTick, onMounted, watch } from 'vue'
import uCharts from '@qiun/ucharts'
import EmptyState from './EmptyState.vue'

const props = defineProps({
  chartType: {
    type: String,
    default: 'line'
  },
  categories: {
    type: Array,
    default: () => []
  },
  series: {
    type: Array,
    default: () => []
  },
  height: {
    type: Number,
    default: 360
  },
  color: {
    type: Array,
    default: () => ['#5c8f5f', '#5f93c9', '#dc8a3a', '#c95c4a']
  },
  unit: {
    type: String,
    default: ''
  }
})

const instance = getCurrentInstance()
const canvasId = `warm-chart-${Math.random().toString(36).slice(2, 9)}`
let chart = null

const hasData = computed(() => props.series.some((item) => Array.isArray(item.data) && item.data.length > 0))

onMounted(draw)

watch(
  () => [props.chartType, props.categories, props.series],
  () => draw(),
  { deep: true }
)

function draw() {
  if (!hasData.value) return
  nextTick(() => {
    const width = uni.getSystemInfoSync().windowWidth - 56
    const context = uni.createCanvasContext(canvasId, instance?.proxy)
    chart = new uCharts({
      type: props.chartType,
      context,
      canvasId,
      width,
      height: props.height / 2,
      categories: props.categories,
      series: props.series,
      animation: true,
      background: '#fffaf1',
      color: props.color,
      padding: [14, 12, 8, 8],
      dataLabel: false,
      legend: { show: false },
      xAxis: {
        disableGrid: true,
        fontColor: '#8a9385'
      },
      yAxis: {
        gridType: 'dash',
        dashLength: 4,
        fontColor: '#8a9385',
        data: [{ min: 0, title: props.unit }]
      },
      extra: {
        line: {
          type: 'curve',
          width: 3,
          activeType: 'hollow',
          linearType: 'custom'
        },
        column: {
          type: 'group',
          width: 26,
          activeBgColor: '#f5eadb'
        }
      }
    })
  })
}

function touchChart(event) {
  chart?.showToolTip(event)
}
</script>

<style scoped>
.chart-card {
  width: 100%;
}
.chart-canvas {
  width: 100%;
  height: 360rpx;
}
</style>
