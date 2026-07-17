<template>
  <view class="page">
    <WarmSectionHeader
      eyebrow="GLUCOSE"
      title="血糖记录"
      desc="把每一次测量按时间放好，趋势会比单个数字更会说话。"
    />

    <view class="panel section">
      <WarmSectionHeader title="最近 7 次趋势" desc="轻点图表可以查看具体数值。" />
      <TrendChart
        chart-type="line"
        unit="mmol/L"
        :categories="trend.categories"
        :series="trend.series"
      />
    </view>

    <view class="panel section">
      <WarmSectionHeader :title="editingRecordId ? '编辑记录' : '新增记录'" desc="测量类型会影响判断，请尽量按实际餐前餐后选择。" />
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
        <input
          class="input value-input"
          :value="form.glucoseValue"
          type="text"
          placeholder="例如 6.8"
          @input="onGlucoseInput"
        />
      </view>
      <view class="field">
        <text class="label">备注</text>
        <input class="input" v-model="form.remark" placeholder="例如 饭后散步 20 分钟" />
      </view>
      <view class="submit">
        <wd-button type="primary" block @click="save">{{ editingRecordId ? '保存修改' : '保存记录' }}</wd-button>
        <wd-button v-if="editingRecordId" class="cancel-btn" plain block @click="cancelEdit">取消编辑</wd-button>
      </view>
    </view>

    <view class="section">
      <WarmSectionHeader title="记录时间线" desc="颜色会帮你快速看出正常、偏高或偏低。" />
      <EmptyState
        v-if="records.length === 0"
        icon="+"
        title="还没有血糖记录"
        desc="添加第一条记录后，这里会变成你的血糖时间线。"
      />
      <view v-else class="card-list">
        <view class="panel record-card" v-for="item in records" :key="item.recordId">
          <view class="record-head">
            <view>
              <text class="record-value">{{ item.glucoseValue }} mmol/L</text>
              <text class="record-time">{{ item.measureType }} · {{ formatTimeLabel(item.measureTime) }}</text>
            </view>
            <StatusPill :text="item.glucoseStatus" :tone="glucoseStatusTone(item.glucoseStatus)" />
          </view>
          <text v-if="item.remark" class="record-remark">{{ item.remark }}</text>
          <view class="record-actions">
            <text class="action edit" @tap="startEdit(item)">编辑</text>
            <text class="action delete" @tap="removeRecord(item)">删除</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'
import { buildGlucoseTrend, formatTimeLabel, glucoseStatusTone } from '../../utils/view-models'

const measureTypes = ['空腹', '早餐后', '午餐前', '午餐后', '晚餐前', '晚餐后', '睡前']
const records = ref([])
const user = ref(null)
const editingRecordId = ref(null)
const now = new Date()
const form = reactive({
  date: formatDate(now),
  time: formatTime(now),
  measureType: '空腹',
  glucoseValue: '',
  remark: ''
})

const trend = computed(() => buildGlucoseTrend(records.value, 7))

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await loadRecords()
})

async function save() {
  const glucoseValue = normalizeGlucoseValue(form.glucoseValue)
  if (!glucoseValue || glucoseValue <= 0) {
    uni.showToast({ title: '请输入有效血糖值', icon: 'none' })
    return
  }
  const payload = {
    userId: user.value.userId,
    measureTime: `${form.date} ${form.time}:00`,
    measureType: form.measureType,
    glucoseValue,
    remark: form.remark
  }
  if (editingRecordId.value) {
    await api.updateGlucose(editingRecordId.value, payload)
    uni.showToast({ title: '已修改', icon: 'success' })
  } else {
    await api.createGlucose(payload)
    uni.showToast({ title: '已保存', icon: 'success' })
  }
  resetForm()
  await loadRecords()
}

async function loadRecords() {
  records.value = await api.listGlucose({ userId: user.value.userId })
}

function formatDate(date) {
  return date.toISOString().slice(0, 10)
}

function formatTime(date) {
  return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
}

function onGlucoseInput(event) {
  form.glucoseValue = sanitizeDecimalInput(event.detail.value)
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

function startEdit(item) {
  editingRecordId.value = item.recordId
  const [datePart, timePart = ''] = String(item.measureTime || '').split(' ')
  form.date = datePart || formatDate(new Date())
  form.time = timePart.slice(0, 5) || formatTime(new Date())
  form.measureType = item.measureType
  form.glucoseValue = String(item.glucoseValue)
  form.remark = item.remark || ''
}

function cancelEdit() {
  resetForm()
}

function resetForm() {
  editingRecordId.value = null
  form.glucoseValue = ''
  form.remark = ''
}

function removeRecord(item) {
  uni.showModal({
    title: '删除血糖记录',
    content: `确认删除 ${item.glucoseValue} mmol/L 这条记录吗？`,
    success: async (res) => {
      if (!res.confirm) return
      await api.deleteGlucose(item.recordId)
      if (editingRecordId.value === item.recordId) resetForm()
      uni.showToast({ title: '已删除', icon: 'success' })
      await loadRecords()
    }
  })
}
</script>

<style scoped>
.submit {
  margin-top: 30rpx;
}
.cancel-btn {
  margin-top: 18rpx;
}
.value-input {
  color: #4f7f53;
  font-size: 36rpx;
  font-weight: 900;
}
.record-card {
  position: relative;
  overflow: hidden;
}
.record-card::before {
  position: absolute;
  top: 28rpx;
  left: 0;
  width: 8rpx;
  height: 72rpx;
  border-radius: 999rpx;
  background: #7faa6f;
  content: '';
}
.record-head {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  align-items: flex-start;
}
.record-value {
  display: block;
  color: #253528;
  font-size: 38rpx;
  font-weight: 900;
}
.record-time,
.record-remark {
  display: block;
  margin-top: 8rpx;
  color: #778276;
  font-size: 25rpx;
  line-height: 1.5;
}
.record-actions {
  display: flex;
  justify-content: flex-end;
  gap: 26rpx;
  margin-top: 18rpx;
}
.action {
  font-size: 24rpx;
  font-weight: 900;
}
.action.edit {
  color: #4f7f53;
}
.action.delete {
  color: #bd4a38;
}
</style>
