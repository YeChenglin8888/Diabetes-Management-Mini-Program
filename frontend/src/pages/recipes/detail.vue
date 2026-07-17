<template>
  <view class="page">
    <view v-if="recipe" class="detail-hero">
      <view :class="['hero-cover', recipeCover(recipe).tone]">
        <text>{{ recipeCover(recipe).icon }}</text>
      </view>
      <view class="hero-text">
        <text class="title">{{ recipe.recipeName }}</text>
        <view class="tags">
          <StatusPill v-for="tag in recipeTags(recipe)" :key="tag" :text="tag" tone="soft" />
        </view>
      </view>
    </view>

    <view v-if="recipe" class="panel section">
      <WarmSectionHeader title="推荐理由" desc="先知道为什么适合，再决定要不要做。" />
      <text class="body">{{ recipe.recommendReason }}</text>
    </view>

    <view v-if="recipe" class="panel section">
      <WarmSectionHeader title="食材" desc="做饭前先对照一下准备情况。" />
      <text class="body">{{ recipe.ingredients }}</text>
    </view>

    <view v-if="recipe" class="panel section">
      <WarmSectionHeader title="做法" desc="步骤尽量简单，适合日常执行。" />
      <text class="body">{{ recipe.steps }}</text>
    </view>

    <view v-if="recipe" class="panel section">
      <WarmSectionHeader title="适用说明" />
      <text class="body">{{ recipe.suitablePeople || '适合需要控糖饮食参考的人群。若存在特殊疾病或医嘱，请以医生建议为准。' }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../api'
import { recipeCover, recipeTags } from '../../utils/view-models'

const recipe = ref(null)

onLoad(async (query) => {
  recipe.value = await api.getRecipe(query.recipeId)
})
</script>

<style scoped>
.detail-hero {
  display: flex;
  gap: 24rpx;
  align-items: center;
  margin-bottom: 24rpx;
  padding: 30rpx;
  border-radius: 38rpx;
  background: linear-gradient(135deg, #fff2df, #eaf4e7);
  box-shadow: 0 20rpx 54rpx rgba(104, 109, 76, 0.12);
}
.hero-cover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 144rpx;
  height: 144rpx;
  flex: 0 0 auto;
  border-radius: 36rpx;
  background: linear-gradient(135deg, #fff0d9, #f2c780);
}
.hero-cover.leaf {
  background: linear-gradient(135deg, #e5f2df, #9ec58f);
}
.hero-cover.night {
  background: linear-gradient(135deg, #e8f1ff, #9ab7df);
}
.hero-cover.snack {
  background: linear-gradient(135deg, #f6eadb, #d1aa77);
}
.hero-cover text {
  color: #ffffff;
  font-size: 48rpx;
  font-weight: 900;
}
.hero-text {
  flex: 1;
  min-width: 0;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 16rpx;
}
.body {
  display: block;
  color: #4d5d4c;
  font-size: 29rpx;
  line-height: 1.85;
}
</style>
