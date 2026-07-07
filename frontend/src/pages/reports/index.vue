<template>
  <view class="page">
    <view class="section">
      <text class="title">数据周报</text>
      <text class="subtle">汇总一周血糖、异常次数和碳水摄入。</text>
    </view>

    <view class="panel section">
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

    <view v-if="report" class="panel">
      <view class="grid">
        <view class="metric">
          <text class="subtle">平均血糖</text>
          <text class="value">{{ report.avgGlucose || '--' }}</text>
        </view>
        <view class="metric">
          <text class="subtle">总碳水</text>
          <text class="value">{{ report.totalCarb }}</text>
        </view>
        <view class="metric">
          <text class="subtle">偏高次数</text>
          <text class="value warn">{{ report.highCount }}</text>
        </view>
        <view class="metric">
          <text class="subtle">偏低次数</text>
          <text class="value danger">{{ report.lowCount }}</text>
        </view>
      </view>
      <text class="heading">饮食建议</text>
      <text class="body">{{ report.suggestion }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'

const user = ref(null)
const report = ref(null)
const range = defaultWeek()
const weekStart = ref(range.start)
const weekEnd = ref(range.end)

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await loadReport()
})

async function loadReport() {
  report.value = await api.getWeeklyReport({
    userId: user.value.userId,
    weekStart: weekStart.value,
    weekEnd: weekEnd.value
  })
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
  margin-top: 24rpx;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.metric {
  padding: 20rpx;
  border-radius: 14rpx;
  background: #f8fafc;
}
.value {
  display: block;
  margin-top: 10rpx;
  color: #0f766e;
  font-size: 42rpx;
  font-weight: 800;
}
.value.warn {
  color: #b54708;
}
.value.danger {
  color: #b42318;
}
.heading {
  display: block;
  margin-top: 28rpx;
  margin-bottom: 10rpx;
  font-weight: 800;
}
.body {
  color: #475467;
  font-size: 28rpx;
  line-height: 1.7;
}
</style>
