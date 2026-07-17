<template>
  <view class="page">
    <WarmSectionHeader
      eyebrow="RECIPES"
      title="降糖食谱"
      desc="不是严格菜单，更像给今天餐桌的一点温柔提醒。"
    />

    <scroll-view scroll-x class="meal-tabs section">
      <view class="meal-tab-wrap">
        <text
          v-for="meal in meals"
          :key="meal"
          :class="['meal-tab', currentMeal === meal ? 'active' : '']"
          @tap="selectMeal(meal)"
        >
          {{ meal }}
        </text>
      </view>
    </scroll-view>

    <EmptyState
      v-if="recipes.length === 0"
      icon="谱"
      title="暂时没有食谱"
      desc="换个餐次看看，或者稍后补充后端食谱数据。"
    />
    <view v-else class="recipe-list">
      <view class="recipe-card" v-for="recipe in recipes" :key="recipe.recipeId" @tap="open(recipe.recipeId)">
        <view :class="['recipe-cover', recipeCover(recipe).tone]">
          <text>{{ recipeCover(recipe).icon }}</text>
        </view>
        <view class="recipe-main">
          <view class="recipe-head">
            <text class="recipe-name">{{ recipe.recipeName }}</text>
            <text class="arrow">›</text>
          </view>
          <text class="reason">{{ recipe.recommendReason }}</text>
          <view class="tags">
            <StatusPill v-for="tag in recipeTags(recipe)" :key="tag" :text="tag" tone="soft" />
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { recipeCover, recipeTags } from '../../utils/view-models'

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
  white-space: nowrap;
}
.meal-tab-wrap {
  display: inline-flex;
  gap: 14rpx;
  padding-bottom: 4rpx;
}
.meal-tab {
  display: inline-flex;
  padding: 16rpx 26rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.78);
  color: #778276;
  font-size: 26rpx;
  font-weight: 800;
}
.meal-tab.active {
  background: #dfeedd;
  color: #4f7f53;
}
.recipe-list {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}
.recipe-card {
  display: flex;
  gap: 20rpx;
  padding: 22rpx;
  border: 1rpx solid rgba(113, 134, 101, 0.1);
  border-radius: 32rpx;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 16rpx 42rpx rgba(97, 106, 78, 0.08);
}
.recipe-cover {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 132rpx;
  min-height: 132rpx;
  flex: 0 0 auto;
  border-radius: 30rpx;
  background: linear-gradient(135deg, #fff0d9, #f8d6a8);
}
.recipe-cover.leaf {
  background: linear-gradient(135deg, #e5f2df, #b9d7ae);
}
.recipe-cover.night {
  background: linear-gradient(135deg, #e8f1ff, #b8cbe8);
}
.recipe-cover.snack {
  background: linear-gradient(135deg, #f6eadb, #e4c9a6);
}
.recipe-cover text {
  color: #ffffff;
  font-size: 44rpx;
  font-weight: 900;
}
.recipe-main {
  flex: 1;
  min-width: 0;
}
.recipe-head {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  align-items: center;
}
.recipe-name {
  color: #253528;
  font-size: 31rpx;
  font-weight: 900;
}
.arrow {
  color: #c97827;
  font-size: 42rpx;
  line-height: 1;
}
.reason {
  display: block;
  margin-top: 10rpx;
  color: #778276;
  font-size: 25rpx;
  line-height: 1.55;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10rpx;
  margin-top: 16rpx;
}
</style>
