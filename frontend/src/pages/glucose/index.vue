<template>
  <view class="page">
    <view class="section">
      <text class="title">血糖记录</text>
      <text class="subtle">录入测量时间、类型和血糖值，系统自动判断状态。</text>
    </view>

    <view class="panel section">
      <view class="row field">
        <view class="grow">
          <text class="label">测量日期</text>
          <picker mode="date" @change="form.date = $event.detail.value">
            <view class="picker">{{ form.date }}</view>
          </picker>
        </view>
        <view class="grow">
          <text class="label">测量时间</text>
          <picker mode="time" @change="form.time = $event.detail.value">
            <view class="picker">{{ form.time }}</view>
          </picker>
        </view>
      </view>
      <view class="field">
        <text class="label">测量类型</text>
        <picker :range="measureTypes" @change="form.measureType = measureTypes[$event.detail.value]">
          <view class="picker">{{ form.measureType }}</view>
        </picker>
      </view>
      <view class="field">
        <text class="label">血糖值 mmol/L</text>
        <input class="input" v-model.number="form.glucoseValue" type="digit" placeholder="例如 6.8" />
      </view>
      <view class="field">
        <text class="label">备注</text>
        <input class="input" v-model="form.remark" placeholder="可选" />
      </view>
      <view class="submit">
        <wd-button type="primary" block @click="save">保存记录</wd-button>
      </view>
    </view>

    <view class="card-list">
      <view class="panel" v-for="item in records" :key="item.recordId">
        <view class="record-head">
          <text class="record-value">{{ item.glucoseValue }} mmol/L</text>
          <text :class="statusClass(item.glucoseStatus)">{{ item.glucoseStatus }}</text>
        </view>
        <text class="subtle">{{ item.measureType }} · {{ item.measureTime }}</text>
        <text v-if="item.remark" class="subtle">{{ item.remark }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'

const measureTypes = ['空腹', '早餐后', '午餐前', '午餐后', '晚餐前', '晚餐后', '睡前']
const records = ref([])
const user = ref(null)
const now = new Date()
const form = reactive({
  date: formatDate(now),
  time: formatTime(now),
  measureType: '空腹',
  glucoseValue: '',
  remark: ''
})

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await loadRecords()
})

async function save() {
  if (!form.glucoseValue || Number(form.glucoseValue) <= 0) {
    uni.showToast({ title: '请输入有效血糖值', icon: 'none' })
    return
  }
  await api.createGlucose({
    userId: user.value.userId,
    measureTime: `${form.date} ${form.time}:00`,
    measureType: form.measureType,
    glucoseValue: Number(form.glucoseValue),
    remark: form.remark
  })
  form.glucoseValue = ''
  form.remark = ''
  await loadRecords()
}

async function loadRecords() {
  records.value = await api.listGlucose({ userId: user.value.userId })
}

function statusClass(status) {
  if (status === '偏高') return 'status warn'
  if (status === '偏低') return 'status danger'
  return 'status'
}

function formatDate(date) {
  return date.toISOString().slice(0, 10)
}

function formatTime(date) {
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}
</script>

<style scoped>
.submit {
  margin-top: 28rpx;
}
.record-head {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  align-items: center;
  margin-bottom: 10rpx;
}
.record-value {
  font-size: 34rpx;
  font-weight: 800;
  color: #101828;
}
</style>
