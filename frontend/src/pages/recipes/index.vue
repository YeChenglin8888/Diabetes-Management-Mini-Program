<template>
  <view class="page">
    <view class="section">
      <text class="title">降糖食谱</text>
      <text class="subtle">按餐次查看低 GI、低碳水、高纤维食谱。</text>
    </view>

    <view class="meal-tabs section">
      <text
        v-for="meal in meals"
        :key="meal"
        :class="['meal-tab', currentMeal === meal ? 'active' : '']"
        @tap="selectMeal(meal)"
      >
        {{ meal }}
      </text>
    </view>

    <view class="card-list">
      <view class="panel recipe-card" v-for="recipe in recipes" :key="recipe.recipeId" @tap="open(recipe.recipeId)">
        <view class="record-head">
          <text class="recipe-name">{{ recipe.recipeName }}</text>
          <text class="status">{{ recipe.mealType }}</text>
        </view>
        <text class="subtle">{{ recipe.recommendReason }}</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'

const meals = ['全部', '早餐', '午餐', '晚餐', '加餐']
const currentMeal = ref('全部')
const recipes = ref([])

onShow(load)

async function load() {
  recipes.value = await api.listRecipes(currentMeal.value === '全部' ? {} : { mealType: currentMeal.value })
}

async function selectMeal(meal) {
  currentMeal.value = meal
  await load()
}

function open(recipeId) {
  uni.navigateTo({ url: `/pages/recipes/detail?recipeId=${recipeId}` })
}
</script>

<style scoped>
.meal-tabs {
  display: flex;
  gap: 14rpx;
  overflow-x: auto;
}
.meal-tab {
  flex: 0 0 auto;
  padding: 14rpx 24rpx;
  border-radius: 999rpx;
  background: #ffffff;
  color: #667085;
  font-size: 26rpx;
}
.meal-tab.active {
  background: #d9f5ef;
  color: #0f766e;
  font-weight: 700;
}
.record-head {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  margin-bottom: 12rpx;
}
.recipe-name {
  font-size: 32rpx;
  font-weight: 800;
}
</style>
