<template>
  <view class="page">
    <view v-if="recipe" class="panel">
      <text class="title">{{ recipe.recipeName }}</text>
      <view class="detail-line">
        <text class="status">{{ recipe.mealType }}</text>
      </view>
      <text class="heading">食材</text>
      <text class="body">{{ recipe.ingredients }}</text>
      <text class="heading">做法</text>
      <text class="body">{{ recipe.steps }}</text>
      <text class="heading">推荐理由</text>
      <text class="body">{{ recipe.recommendReason }}</text>
      <text class="heading">适用说明</text>
      <text class="body">{{ recipe.suitablePeople || '适合需要控糖饮食参考的人群' }}</text>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { api } from '../../api'

const recipe = ref(null)

onLoad(async (query) => {
  recipe.value = await api.getRecipe(query.recipeId)
})
</script>

<style scoped>
.detail-line {
  margin: 18rpx 0 28rpx;
}
.heading {
  display: block;
  margin-top: 26rpx;
  margin-bottom: 10rpx;
  color: #101828;
  font-size: 30rpx;
  font-weight: 800;
}
.body {
  display: block;
  color: #475467;
  font-size: 28rpx;
  line-height: 1.7;
}
</style>
