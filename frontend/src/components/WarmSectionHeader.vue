<template>
  <view class="section-head">
    <view>
      <text v-if="eyebrow" class="eyebrow">{{ eyebrow }}</text>
      <text class="heading">{{ title }}</text>
      <text v-if="desc" class="desc">{{ desc }}</text>
    </view>
    <slot />
  </view>
</template>

<script setup>
defineProps({
  eyebrow: {
    type: String,
    default: ''
  },
  title: {
    type: String,
    default: ''
  },
  desc: {
    type: String,
    default: ''
  }
})
</script>

<style scoped>
.section-head {
  display: flex;
  justify-content: space-between;
  gap: 18rpx;
  align-items: flex-start;
  margin-bottom: 18rpx;
}
.eyebrow {
  display: block;
  margin-bottom: 6rpx;
  color: #d27a2c;
  font-size: 22rpx;
  font-weight: 800;
}
.heading {
  display: block;
  color: #253528;
  font-size: 34rpx;
  font-weight: 900;
  line-height: 1.25;
}
.desc {
  display: block;
  margin-top: 8rpx;
  color: #778276;
  font-size: 25rpx;
  line-height: 1.55;
}
</style>
