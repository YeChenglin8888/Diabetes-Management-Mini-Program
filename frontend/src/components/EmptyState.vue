<template>
  <view class="empty-state">
    <view class="empty-mark">{{ icon }}</view>
    <text class="empty-title">{{ title }}</text>
    <text v-if="desc" class="empty-desc">{{ desc }}</text>
  </view>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: '+'
  },
  title: {
    type: String,
    default: '暂无数据'
  },
  desc: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.empty-state {
  padding: 42rpx 28rpx;
  border: 2rpx dashed rgba(138, 154, 134, 0.34);
  border-radius: 28rpx;
  background: rgba(255, 251, 243, 0.72);
  text-align: center;
}
.empty-mark {
  width: 86rpx;
  height: 86rpx;
  margin: 0 auto 18rpx;
  border-radius: 28rpx;
  background: #f8e8cf;
  color: #c97827;
  line-height: 86rpx;
  font-size: 36rpx;
  font-weight: 900;
}
.empty-title {
  display: block;
  color: #334136;
  font-size: 30rpx;
  font-weight: 900;
}
.empty-desc {
  display: block;
  margin-top: 8rpx;
  color: #7e897b;
  font-size: 25rpx;
  line-height: 1.55;
}
</style>
