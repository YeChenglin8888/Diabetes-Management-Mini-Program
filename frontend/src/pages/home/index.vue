<template>
  <view class="page">
    <view class="today-hero">
      <view class="hero-copy">
        <text class="hello">早安，{{ user?.username || '患者' }}</text>
        <text class="hero-title">记录血糖，看看今天的节奏。</text>
        <text class="hero-subtitle">最近一次：{{ latestGlucose ? `${latestGlucose.measureType} ${latestGlucose.glucoseValue} mmol/L` : '还没有记录' }}</text>
      </view>
      <StatusPill :text="latestGlucose?.glucoseStatus || '待记录'" :tone="glucoseStatusTone(latestGlucose?.glucoseStatus)" />
    </view>

    <view class="metric-grid section">
      <HealthMetricCard
        label="最近血糖"
        :value="latestGlucose ? latestGlucose.glucoseValue : '--'"
        unit="mmol/L"
        :hint="latestGlucose ? latestGlucose.measureType : '先记录一条血糖'"
        icon="糖"
        tone="green"
      />
      <HealthMetricCard
        label="今日碳水"
        :value="todayNutrition.carb"
        unit="g"
        hint="已记录饮食汇总"
        icon="碳"
        tone="orange"
      />
    </view>

    <view class="panel section glucose-panel">
      <WarmSectionHeader title="记录血糖" desc="选择类型，输入数值即可保存。">
        <wd-button size="small" plain @click="go('/pages/glucose/index')">明细</wd-button>
      </WarmSectionHeader>
      <view class="row field">
        <view class="grow">
          <text class="label">日期</text>
          <picker mode="date" @change="glucoseForm.date = $event.detail.value">
            <view class="picker">{{ glucoseForm.date }}</view>
          </picker>
        </view>
        <view class="grow">
          <text class="label">时间</text>
          <picker mode="time" @change="glucoseForm.time = $event.detail.value">
            <view class="picker">{{ glucoseForm.time }}</view>
          </picker>
        </view>
      </view>
      <view class="row field">
        <view class="grow">
          <text class="label">类型</text>
          <picker :range="measureTypes" @change="glucoseForm.measureType = measureTypes[$event.detail.value]">
            <view class="picker">{{ glucoseForm.measureType }}</view>
          </picker>
        </view>
        <view class="grow">
          <text class="label">血糖 mmol/L</text>
          <input
            class="input value-input"
            :value="glucoseForm.glucoseValue"
            type="text"
            placeholder="例如 6.8"
            @input="onGlucoseInput"
          />
        </view>
      </view>
      <view class="field">
        <text class="label">备注</text>
        <input class="input" v-model="glucoseForm.remark" placeholder="例如 饭后散步 20 分钟" />
      </view>
      <view class="submit">
        <wd-button type="primary" block :loading="savingGlucose" @click="saveGlucose">保存血糖</wd-button>
      </view>
    </view>

    <view class="panel section">
      <WarmSectionHeader title="今日营养" desc="按已保存的饮食记录汇总。" />
      <view class="nutrition-grid">
        <view class="nutrition-item">
          <text class="nutrition-value">{{ todayNutrition.carb }}g</text>
          <text class="nutrition-label">碳水</text>
        </view>
        <view class="nutrition-item">
          <text class="nutrition-value">{{ todayNutrition.protein }}g</text>
          <text class="nutrition-label">蛋白质</text>
        </view>
        <view class="nutrition-item">
          <text class="nutrition-value">{{ todayNutrition.fastCarb }}g</text>
          <text class="nutrition-label">快碳</text>
        </view>
      </view>
      <text class="nutrition-hint">{{ nutritionHint }}</text>
    </view>

  </view>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'
import { glucoseStatusTone } from '../../utils/view-models'

const user = ref(null)
const latestGlucose = ref(null)
const measureTypes = ['空腹', '早餐后', '午餐前', '午餐后', '晚餐前', '晚餐后', '睡前']
const savingGlucose = ref(false)
const now = new Date()
const glucoseForm = reactive({
  date: formatDate(now),
  time: formatTime(now),
  measureType: '空腹',
  glucoseValue: '',
  remark: ''
})
const todayNutrition = ref({ carb: '0.0', protein: '0.0', fastCarb: '0.0' })
const nutritionHint = ref('今天还没有饮食记录，先保存一餐看看结构。')

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await Promise.all([loadLatest(), loadTodayNutrition()])
})

async function loadLatest() {
  const list = await api.listGlucose({ userId: user.value.userId })
  latestGlucose.value = list[0] || null
}

async function saveGlucose() {
  const glucoseValue = normalizeGlucoseValue(glucoseForm.glucoseValue)
  if (!glucoseValue || glucoseValue <= 0) {
    uni.showToast({ title: '请输入有效血糖值', icon: 'none' })
    return
  }
  savingGlucose.value = true
  try {
    await api.createGlucose({
      userId: user.value.userId,
      measureTime: `${glucoseForm.date} ${glucoseForm.time}:00`,
      measureType: glucoseForm.measureType,
      glucoseValue,
      remark: glucoseForm.remark
    })
    uni.showToast({ title: '已保存', icon: 'success' })
    glucoseForm.glucoseValue = ''
    glucoseForm.remark = ''
    await loadLatest()
  } finally {
    savingGlucose.value = false
  }
}

function onGlucoseInput(event) {
  glucoseForm.glucoseValue = sanitizeDecimalInput(event.detail.value)
}

function sanitizeDecimalInput(value) {
  const text = String(value || '').replace(/[^\d.]/g, '')
  const [integerPart, ...decimalParts] = text.split('.')
  const decimalPart = decimalParts.join('').slice(0, 1)
  if (text.includes('.')) {
    return `${integerPart}.${decimalPart}`
  }
  return integerPart.slice(0, 3)
}

function normalizeGlucoseValue(value) {
  if (value === '.' || value === '') return null
  const normalized = String(value).startsWith('.') ? `0${value}` : String(value)
  const number = Number(normalized)
  return Number.isFinite(number) ? Number(number.toFixed(1)) : null
}

async function loadTodayNutrition() {
  const today = new Date().toISOString().slice(0, 10)
  const list = await api.listDiets({ userId: user.value.userId, startDate: today, endDate: today })
  const carb = list.reduce((sum, item) => sum + Number(item.totalCarb || 0), 0)
  const protein = list.reduce((sum, item) => sum + Number(item.totalProtein || 0), 0)
  const fastCarb = list.reduce((sum, item) => sum + Number(item.fastCarbTotal || 0), 0)
  todayNutrition.value = {
    carb: carb.toFixed(1),
    protein: protein.toFixed(1),
    fastCarb: fastCarb.toFixed(1)
  }
  if (list.length === 0) {
    nutritionHint.value = '今天还没有饮食记录，先保存一餐看看结构。'
  } else if (fastCarb > 30) {
    nutritionHint.value = '今天快碳偏多，下一餐可以多放蔬菜和优质蛋白。'
  } else {
    nutritionHint.value = '今天饮食结构记录得不错，继续保持完整记录。'
  }
}

function go(url) {
  uni.navigateTo({ url })
}

function formatDate(date) {
  return date.toISOString().slice(0, 10)
}

function formatTime(date) {
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.today-hero {
  display: flex;
  justify-content: space-between;
  gap: 22rpx;
  align-items: center;
  margin-bottom: 22rpx;
  padding: 34rpx 30rpx;
  border-radius: 34rpx;
  background: linear-gradient(135deg, #fdf1dc 0%, #e8f4e6 100%);
  box-shadow: 0 18rpx 46rpx rgba(98, 112, 83, 0.12);
}
.hero-copy {
  flex: 1;
  min-width: 0;
}
.hello {
  display: block;
  color: #c97827;
  font-size: 24rpx;
  font-weight: 900;
}
.hero-title {
  display: block;
  margin-top: 10rpx;
  color: #26382a;
  font-size: 38rpx;
  font-weight: 900;
  line-height: 1.24;
}
.hero-subtitle {
  display: block;
  margin-top: 12rpx;
  color: #667263;
  font-size: 25rpx;
  line-height: 1.45;
}
.metric-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.nutrition-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14rpx;
}
.nutrition-item {
  padding: 20rpx 12rpx;
  border-radius: 22rpx;
  background: #f7fbf5;
  text-align: center;
}
.nutrition-value,
.nutrition-label,
.nutrition-hint {
  display: block;
}
.nutrition-value {
  color: #26382a;
  font-size: 30rpx;
  font-weight: 900;
}
.nutrition-label {
  margin-top: 6rpx;
  color: #778276;
  font-size: 22rpx;
}
.nutrition-hint {
  margin-top: 18rpx;
  color: #6b7568;
  font-size: 25rpx;
  line-height: 1.6;
}
.glucose-panel {
  background: rgba(255, 255, 255, 0.94);
}
.submit {
  margin-top: 26rpx;
}
.value-input {
  color: #4f7f53;
  font-size: 34rpx;
  font-weight: 900;
}
</style>
