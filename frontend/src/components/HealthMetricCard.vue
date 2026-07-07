<template>
  <view :class="['metric-card', tone]">
    <view class="metric-top">
      <text class="label">{{ label }}</text>
      <text v-if="icon" class="icon">{{ icon }}</text>
    </view>
    <view class="metric-main">
      <text class="value">{{ value }}</text>
      <text v-if="unit" class="unit">{{ unit }}</text>
    </view>
    <text v-if="hint" class="hint">{{ hint }}</text>
  </view>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  unit: String,
  hint: String,
  icon: String,
  tone: {
    type: String,
    default: 'green'
  }
})
</script>

<style scoped>
.metric-card {
  min-height: 168rpx;
  box-sizing: border-box;
  padding: 24rpx;
  border: 1rpx solid rgba(77, 103, 80, 0.08);
  border-radius: 28rpx;
  background: linear-gradient(145deg, #ffffff, #f4fbf4);
  box-shadow: 0 16rpx 40rpx rgba(67, 84, 65, 0.08);
}
.metric-card.blue {
  background: linear-gradient(145deg, #ffffff, #edf5ff);
}
.metric-card.orange {
  background: linear-gradient(145deg, #ffffff, #fff1df);
}
.metric-card.red {
  background: linear-gradient(145deg, #ffffff, #ffefeb);
}
.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14rpx;
}
.label {
  color: #6f7d70;
  font-size: 24rpx;
  font-weight: 700;
}
.icon {
  width: 46rpx;
  height: 46rpx;
  border-radius: 16rpx;
  background: rgba(255, 255, 255, 0.72);
  color: #d27a2c;
  text-align: center;
  line-height: 46rpx;
  font-size: 24rpx;
  font-weight: 900;
}
.metric-main {
  display: flex;
  align-items: baseline;
  gap: 8rpx;
  margin-top: 18rpx;
}
.value {
  color: #233629;
  font-size: 48rpx;
  font-weight: 900;
  line-height: 1;
}
.unit {
  color: #778276;
  font-size: 22rpx;
}
.hint {
  display: block;
  margin-top: 14rpx;
  color: #87917f;
  font-size: 23rpx;
  line-height: 1.45;
}
</style>
