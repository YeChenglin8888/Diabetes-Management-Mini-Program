<template>
  <view class="page">
    <view class="section">
      <text class="title">今日概览</text>
      <text class="subtle">你好，{{ user?.username || '患者' }}</text>
    </view>

    <view class="grid section">
      <view class="metric panel">
        <text class="subtle">最近血糖</text>
        <text class="value">{{ latestGlucose ? latestGlucose.glucoseValue : '--' }}</text>
        <text class="unit">mmol/L</text>
      </view>
      <view class="metric panel">
        <text class="subtle">血糖状态</text>
        <text :class="statusClass(latestGlucose?.glucoseStatus)">
          {{ latestGlucose?.glucoseStatus || '暂无' }}
        </text>
      </view>
    </view>

    <view class="panel section">
      <text class="block-title">快捷入口</text>
      <view class="actions">
        <wd-button type="primary" @click="goTab('/pages/glucose/index')">记录血糖</wd-button>
        <wd-button type="success" @click="goTab('/pages/diet/index')">饮食测算</wd-button>
        <wd-button plain @click="go('/pages/recipes/index')">降糖食谱</wd-button>
        <wd-button plain @click="goTab('/pages/reports/index')">数据周报</wd-button>
      </view>
    </view>

    <view class="panel">
      <text class="block-title">联调状态</text>
      <text class="subtle">后端服务：{{ healthText }}</text>
      <wd-button size="small" custom-class="check-btn" @click="checkHealth">重新检测</wd-button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'

const user = ref(null)
const latestGlucose = ref(null)
const healthText = ref('检测中')

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await Promise.all([loadLatest(), checkHealth()])
})

async function loadLatest() {
  const list = await api.listGlucose({ userId: user.value.userId })
  latestGlucose.value = list[0] || null
}

async function checkHealth() {
  try {
    await api.health()
    healthText.value = '正常'
  } catch {
    healthText.value = '未连接'
  }
}

function go(url) {
  uni.navigateTo({ url })
}

function goTab(url) {
  uni.switchTab({ url })
}

function statusClass(status) {
  if (status === '偏高') return 'status warn'
  if (status === '偏低') return 'status danger'
  return 'status'
}
</script>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.metric {
  min-height: 150rpx;
}
.value {
  display: block;
  margin-top: 12rpx;
  color: #0f766e;
  font-size: 52rpx;
  font-weight: 800;
}
.unit {
  color: #667085;
  font-size: 24rpx;
}
.block-title {
  display: block;
  margin-bottom: 18rpx;
  font-size: 30rpx;
  font-weight: 700;
}
.actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.check-btn {
  margin-top: 18rpx;
}
</style>
