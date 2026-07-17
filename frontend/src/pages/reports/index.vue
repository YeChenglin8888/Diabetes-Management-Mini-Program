<template>
  <view class="page">
    <WarmSectionHeader
      eyebrow="WEEKLY"
      title="数据周报"
      desc="一周只看几个关键问题：血糖稳不稳、碳水多不多、下一步做什么。"
    />

    <view class="panel section">
      <WarmSectionHeader title="选择周期" desc="默认展示最近 7 天，也可以自己选择时间范围。" />
      <view class="row">
        <view class="grow">
          <text class="label">周开始</text>
          <picker mode="date" @change="weekStart = $event.detail.value">
            <view class="picker">{{ weekStart }}</view>
          </picker>
        </view>
        <view class="grow">
          <text class="label">周结束</text>
          <picker mode="date" @change="weekEnd = $event.detail.value">
            <view class="picker">{{ weekEnd }}</view>
          </picker>
        </view>
      </view>
      <view class="submit">
        <wd-button type="primary" block @click="loadReport">生成周报</wd-button>
      </view>
    </view>

    <view v-if="report" class="panel ai-card section">
      <WarmSectionHeader title="AI 周报解读" :desc="aiStatusText" />
      <text v-if="aiAnalysis" class="suggestion">{{ aiAnalysis }}</text>
      <text v-else class="page-note">点击按钮后，后端会使用脱敏周报统计调用 deepseek-v4-pro。</text>
      <view class="submit">
        <wd-button type="primary" block :loading="aiLoading" @click="loadAiAnalysis">生成 AI 解读</wd-button>
      </view>
    </view>

    <view v-if="report" class="metric-grid section">
      <HealthMetricCard label="平均血糖" :value="report.avgGlucose || '--'" unit="mmol/L" hint="本周整体水平" icon="糖" tone="green" />
      <HealthMetricCard label="总碳水" :value="report.totalCarb || 0" unit="g" hint="一周饮食估算" icon="碳" tone="orange" />
      <HealthMetricCard label="蛋白质" :value="report.totalProtein || 0" unit="g" hint="本周优质蛋白估算" icon="蛋" tone="green" />
      <HealthMetricCard label="快碳占比" :value="report.fastCarbRatio || 0" unit="%" hint="越高越需要复盘" icon="快" tone="red" />
    </view>

    <view v-if="report" class="panel section">
      <WarmSectionHeader title="碳水概览" desc="用周总量和日均值看饮食负担。" />
      <TrendChart chart-type="column" unit="g" :categories="carbChart.categories" :series="carbChart.series" />
    </view>

    <view v-if="report" class="panel section">
      <WarmSectionHeader title="营养结构" desc="碳水、蛋白质、脂肪和纤维放在一起看，更容易发现搭配问题。" />
      <TrendChart chart-type="column" unit="g" :categories="nutritionChart.categories" :series="nutritionChart.series" />
    </view>

    <view v-if="report" class="metric-grid section">
      <HealthMetricCard label="偏高次数" :value="report.highCount || 0" unit="次" hint="需要复盘的餐次" icon="高" tone="red" />
      <HealthMetricCard label="偏低次数" :value="report.lowCount || 0" unit="次" hint="关注低血糖风险" icon="低" tone="blue" />
      <HealthMetricCard label="膳食纤维" :value="report.totalFiber || 0" unit="g" hint="蔬菜全谷贡献" icon="纤" tone="green" />
      <HealthMetricCard label="慢碳" :value="report.slowCarbTotal || 0" unit="g" hint="更平稳的碳水来源" icon="慢" tone="blue" />
    </view>

    <view v-if="report" class="panel suggestion-card">
      <WarmSectionHeader title="本周建议" desc="系统根据记录给出的课程设计建议。" />
      <text class="suggestion">{{ report.suggestion || fallbackSuggestion }}</text>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'
import { buildCarbChart, buildNutritionChart } from '../../utils/view-models'

const user = ref(null)
const report = ref(null)
const aiConfig = ref(null)
const aiAnalysis = ref('')
const aiLoading = ref(false)
const aiFallback = ref(false)
const range = defaultWeek()
const weekStart = ref(range.start)
const weekEnd = ref(range.end)
const fallbackSuggestion = '继续保持规律记录。若连续出现偏高或偏低，建议结合餐次、运动和用药情况复盘。'
const carbChart = computed(() => buildCarbChart(report.value))
const nutritionChart = computed(() => buildNutritionChart(report.value))
const aiStatusText = computed(() => {
  if (aiFallback.value) return 'AI 服务暂不可用，当前显示规则建议。'
  if (aiConfig.value?.configured) return `已配置 ${aiConfig.value.model || 'AI模型'}，可生成辅助解读。`
  return '请先在后端 .env 配置 AI_API_KEY。'
})
const aiAnalysisCache = new Map()

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await loadAiConfig()
  await loadReport()
})

async function loadReport() {
  restoreAiAnalysis()
  report.value = await api.getWeeklyReport({
    userId: user.value.userId,
    weekStart: weekStart.value,
    weekEnd: weekEnd.value
  })
}

async function loadAiConfig() {
  try {
    aiConfig.value = await api.getAiConfig()
  } catch {
    aiConfig.value = null
  }
}

async function loadAiAnalysis() {
  if (aiLoading.value) return
  aiLoading.value = true
  try {
    const result = await api.generateWeeklyAnalysis({
      userId: user.value.userId,
      weekStart: weekStart.value,
      weekEnd: weekEnd.value
    })
    aiAnalysis.value = result.analysis || fallbackSuggestion
    aiFallback.value = !!result.fallback
    cacheAiAnalysis()
  } finally {
    aiLoading.value = false
  }
}

function cacheAiAnalysis() {
  if (!aiAnalysis.value) return
  aiAnalysisCache.set(aiAnalysisCacheKey(), {
    analysis: aiAnalysis.value,
    fallback: aiFallback.value
  })
}

function restoreAiAnalysis() {
  const cached = aiAnalysisCache.get(aiAnalysisCacheKey())
  aiAnalysis.value = cached?.analysis || ''
  aiFallback.value = !!cached?.fallback
}

function aiAnalysisCacheKey() {
  return `weeklyAiAnalysis:${user.value?.userId || 'guest'}:${weekStart.value}:${weekEnd.value}`
}

function defaultWeek() {
  const end = new Date()
  const start = new Date()
  start.setDate(end.getDate() - 6)
  return { start: formatDate(start), end: formatDate(end) }
}

function formatDate(date) {
  return date.toISOString().slice(0, 10)
}
</script>

<style scoped>
.submit {
  margin-top: 26rpx;
}
.metric-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.suggestion-card {
  background: linear-gradient(145deg, #fffaf0, #edf5ec);
}
.ai-card {
  margin-top: 24rpx;
  background: linear-gradient(145deg, #f7fbf5, #eaf2ff);
}
.suggestion {
  display: block;
  color: #4d5d4c;
  font-size: 29rpx;
  line-height: 1.8;
}
</style>
