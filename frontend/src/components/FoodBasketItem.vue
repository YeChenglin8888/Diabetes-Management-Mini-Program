<template>
  <view class="basket-item">
    <view class="food-mark">{{ index + 1 }}</view>
    <view class="food-main">
      <text class="food-name">{{ item.foodName }}</text>
      <text class="food-meta">
        {{ item.weightG }}g · {{ item.carbValue }}g 碳水 · {{ item.proteinValue || 0 }}g 蛋白
      </text>
      <view class="nutrition-row">
        <text class="tag">{{ item.carbType || '混合碳' }}</text>
        <text class="tag muted">GI {{ item.giLevel || '低' }}</text>
        <text class="tag muted">脂肪 {{ item.fatValue || 0 }}g</text>
        <text class="tag muted">纤维 {{ item.fiberValue || 0 }}g</text>
      </view>
    </view>
    <text class="remove" @tap="$emit('remove')">移除</text>
  </view>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    default: 0
  }
})

defineEmits(['remove'])
</script>

<style scoped>
.basket-item {
  display: flex;
  align-items: center;
  gap: 18rpx;
  padding: 22rpx 0;
  border-bottom: 1rpx solid rgba(139, 154, 137, 0.18);
}
.basket-item:last-child {
  border-bottom: none;
}
.food-mark {
  width: 58rpx;
  height: 58rpx;
  flex: 0 0 auto;
  border-radius: 20rpx;
  background: #eaf4e8;
  color: #4f7f53;
  text-align: center;
  line-height: 58rpx;
  font-size: 24rpx;
  font-weight: 900;
}
.food-main {
  flex: 1;
  min-width: 0;
}
.food-name {
  display: block;
  color: #2d392f;
  font-size: 29rpx;
  font-weight: 900;
}
.food-meta {
  display: block;
  margin-top: 6rpx;
  color: #7b8578;
  font-size: 24rpx;
}
.nutrition-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8rpx;
  margin-top: 12rpx;
}
.tag {
  padding: 5rpx 12rpx;
  border-radius: 999rpx;
  background: #fff0d9;
  color: #b46b20;
  font-size: 21rpx;
  font-weight: 800;
}
.tag.muted {
  background: #f3f6ef;
  color: #6c7769;
}
.remove {
  color: #bd4a38;
  font-size: 24rpx;
  font-weight: 800;
}
</style>
