<template>
  <view class="page">
    <WarmSectionHeader
      eyebrow="MEAL"
      title="饮食测算"
      desc="像往篮子里放食材一样记录本餐，系统会帮你估算三大营养素和快慢碳。"
    />

    <view class="meal-summary section">
      <HealthMetricCard label="本餐碳水" :value="totals.carb" unit="g" hint="保存前可以继续调整" icon="碳" tone="orange" />
      <HealthMetricCard label="蛋白质" :value="totals.protein" unit="g" hint="帮助延缓餐后波动" icon="蛋" tone="green" />
      <HealthMetricCard label="脂肪" :value="totals.fat" unit="g" hint="关注烹调油和坚果" icon="脂" tone="blue" />
      <HealthMetricCard label="膳食纤维" :value="totals.fiber" unit="g" hint="优先来自蔬菜全谷" icon="纤" tone="green" />
    </view>

    <view class="recipe-entry section" @tap="goRecipes">
      <view class="recipe-entry-icon">谱</view>
      <view class="recipe-entry-copy">
        <text class="recipe-entry-title">降糖食谱</text>
        <text class="recipe-entry-desc">先找一份餐单灵感，再回来记录本餐。</text>
      </view>
      <text class="recipe-entry-arrow">›</text>
    </view>

    <view class="panel section">
      <WarmSectionHeader title="添加食物" desc="选择食物后填写重量，马上加入本餐篮子。" />
      <view class="field">
        <text class="label">餐次</text>
        <picker :range="mealTypes" @change="form.mealType = mealTypes[$event.detail.value]">
          <view class="picker">{{ form.mealType }}</view>
        </picker>
      </view>
      <view class="field">
        <text class="label">选择食物</text>
        <picker :range="foodNames" @change="pickFood">
          <view class="picker">{{ selectedFood ? selectedFood.foodName : '请选择食物' }}</view>
        </picker>
      </view>
      <view class="row field recognized-row">
        <view class="grow">
          <text class="label">食物分类</text>
          <view :class="['recognized-value', selectedFood ? 'identified' : '']">{{ recognizedCategory }}</view>
        </view>
        <view class="grow">
          <text class="label">碳水类型</text>
          <view :class="['recognized-value', selectedFood ? 'identified' : '']">{{ recognizedCarbType }}</view>
        </view>
      </view>
      <view v-if="selectedFood" class="food-analysis">
        <view class="analysis-head">
          <text class="analysis-title">{{ selectedFood.foodName }}</text>
          <text class="analysis-pill">{{ selectedFood.carbType }}</text>
        </view>
        <text class="analysis-desc">
          每100g：碳水 {{ selectedFood.carbPer100g }}g、蛋白 {{ selectedFood.proteinPer100g }}g、脂肪 {{ selectedFood.fatPer100g }}g、纤维 {{ selectedFood.fiberPer100g }}g
        </text>
      </view>
      <view class="row field">
        <view class="grow">
          <text class="label">重量 g</text>
          <input class="input" v-model.number="weightG" type="digit" placeholder="例如 100" />
        </view>
        <view class="add-btn">
          <wd-button type="primary" @click="addItem">加入篮子</wd-button>
        </view>
      </view>
    </view>

    <view class="panel section">
      <WarmSectionHeader title="本餐篮子" :desc="items.length ? '确认无误后保存本餐记录。' : '先添加一种食物，篮子会热闹起来。'" />
      <EmptyState v-if="items.length === 0" icon="餐" title="篮子还是空的" desc="添加食物后会显示重量和碳水估算。" />
      <view v-else>
        <FoodBasketItem
          v-for="(item, index) in items"
          :key="`${item.foodId}-${index}`"
          :item="item"
          :index="index"
          @remove="items.splice(index, 1)"
        />
        <view class="carb-bar">
          <view class="carb-fill" :style="{ width: carbPercent + '%' }"></view>
        </view>
        <text class="page-note">按 80g 碳水作为一餐参考上限显示进度，仅用于课程设计演示。</text>
        <view v-if="fastCarbHint" class="hint-card">{{ fastCarbHint }}</view>
      </view>
      <view class="submit">
        <wd-button type="success" block @click="saveDiet">保存饮食记录</wd-button>
      </view>
    </view>

    <view class="panel section">
      <WarmSectionHeader title="最近饮食" desc="保存后的餐次会汇总到周报和首页。" />
      <EmptyState v-if="recentDiets.length === 0" icon="记" title="还没有饮食记录" desc="保存一餐后，这里会显示营养摘要。" />
      <view v-else class="diet-list">
        <view v-for="diet in recentDiets" :key="diet.dietId" class="diet-record">
          <text class="diet-title">{{ diet.mealType }} · {{ formatMealTime(diet.mealTime) }}</text>
          <text class="diet-meta">碳水 {{ diet.totalCarb }}g · 蛋白 {{ diet.totalProtein }}g · 脂肪 {{ diet.totalFat }}g · 纤维 {{ diet.totalFiber }}g</text>
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

const mealTypes = ['早餐', '午餐', '晚餐', '加餐']
const foods = ref([])
const items = ref([])
const recentDiets = ref([])
const selectedFood = ref(null)
const weightG = ref('')
const user = ref(null)
const form = reactive({ mealType: '早餐' })
const foodNames = computed(() => foods.value.map((food) => food.foodName || '未命名食物'))
const recognizedCategory = computed(() => selectedFood.value?.category || '选择食物后自动识别')
const recognizedCarbType = computed(() => selectedFood.value?.carbType || '选择食物后自动识别')
const totals = computed(() => ({
  carb: sumBy('carbValue'),
  protein: sumBy('proteinValue'),
  fat: sumBy('fatValue'),
  fiber: sumBy('fiberValue'),
  calories: sumBy('calories')
}))
const fastCarbTotal = computed(() =>
  Number(items.value.filter((item) => item.carbType === '快碳').reduce((sum, item) => sum + Number(item.carbValue || 0), 0).toFixed(1))
)
const carbPercent = computed(() => Math.min(100, Math.round((Number(totals.value.carb) / 80) * 100)))
const fastCarbHint = computed(() => {
  if (!items.value.length || fastCarbTotal.value === 0) return ''
  const ratio = fastCarbTotal.value / Math.max(Number(totals.value.carb), 1)
  if (ratio >= 0.35) return '本餐快碳占比较高，建议搭配鸡胸肉、酸奶或蔬菜，减少餐后血糖快速上升。'
  return '本餐包含少量快碳，搭配蛋白质和纤维会更稳。'
})

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  foods.value = await api.listFoods()
  await loadRecentDiets()
})

function pickFood(event) {
  selectedFood.value = foods.value[Number(event.detail.value)] || null
}

async function addItem() {
  if (!selectedFood.value || !weightG.value) {
    uni.showToast({ title: '请选择食物并填写重量', icon: 'none' })
    return
  }
  const result = await api.calculateDiet({
    foodId: selectedFood.value.foodId,
    weightG: Number(weightG.value)
  })
  items.value.push(result)
  weightG.value = ''
  uni.showToast({ title: '已加入篮子', icon: 'none' })
}

async function saveDiet() {
  if (items.value.length === 0) {
    uni.showToast({ title: '请先添加食物', icon: 'none' })
    return
  }
  await api.saveDiet({
    userId: user.value.userId,
    mealType: form.mealType,
    mealTime: `${new Date().toISOString().slice(0, 10)} 12:00:00`,
    items: items.value.map((item) => ({ foodId: item.foodId, weightG: item.weightG })),
    remark: ''
  })
  items.value = []
  await loadRecentDiets()
  uni.showToast({ title: '饮食已保存', icon: 'success' })
}

async function loadRecentDiets() {
  recentDiets.value = await api.listDiets({ userId: user.value.userId })
}

function goRecipes() {
  uni.navigateTo({ url: '/pages/recipes/index' })
}

function sumBy(key) {
  return items.value.reduce((sum, item) => sum + Number(item[key] || 0), 0).toFixed(1)
}

function formatMealTime(value) {
  const text = String(value || '')
  return text.includes(' ') ? text.split(' ')[1].slice(0, 5) : text
}
</script>

<style scoped>
.meal-summary {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.add-btn {
  padding-top: 50rpx;
}
.recipe-entry {
  display: flex;
  align-items: center;
  gap: 18rpx;
  box-sizing: border-box;
  padding: 22rpx 24rpx;
  border: 1rpx solid rgba(95, 143, 95, 0.14);
  border-radius: 26rpx;
  background: linear-gradient(135deg, rgba(242, 250, 239, 0.96), rgba(255, 248, 237, 0.94));
  box-shadow: 0 14rpx 34rpx rgba(92, 102, 75, 0.08);
}
.recipe-entry-icon {
  width: 72rpx;
  height: 72rpx;
  flex: 0 0 auto;
  border-radius: 22rpx;
  background: #5c8f5f;
  color: #ffffff;
  font-size: 30rpx;
  font-weight: 900;
  line-height: 72rpx;
  text-align: center;
}
.recipe-entry-copy {
  flex: 1;
  min-width: 0;
}
.recipe-entry-title,
.recipe-entry-desc {
  display: block;
}
.recipe-entry-title {
  color: #26382a;
  font-size: 29rpx;
  font-weight: 900;
}
.recipe-entry-desc {
  margin-top: 6rpx;
  color: #6b7568;
  font-size: 23rpx;
  line-height: 1.45;
}
.recipe-entry-arrow {
  color: #c97827;
  font-size: 46rpx;
  font-weight: 800;
  line-height: 1;
}
.recognized-row {
  align-items: flex-start;
}
.recognized-value {
  box-sizing: border-box;
  width: 100%;
  min-height: 84rpx;
  padding: 0 22rpx;
  border: 1rpx solid rgba(117, 135, 111, 0.16);
  border-radius: 20rpx;
  background: #f8f4eb;
  color: #8b9487;
  font-size: 26rpx;
  line-height: 84rpx;
}
.recognized-value.identified {
  border-color: rgba(95, 143, 95, 0.22);
  background: #f2faef;
  color: #3f6f43;
  font-weight: 900;
}
.carb-bar {
  overflow: hidden;
  height: 18rpx;
  margin: 24rpx 0 12rpx;
  border-radius: 999rpx;
  background: #f1e6d7;
}
.carb-fill {
  height: 100%;
  border-radius: 999rpx;
  background: linear-gradient(90deg, #79a86d, #df9242);
}
.food-analysis,
.hint-card {
  padding: 22rpx;
  border-radius: 24rpx;
  background: #fff8ed;
}
.analysis-head {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  align-items: center;
}
.analysis-title {
  color: #26382a;
  font-size: 28rpx;
  font-weight: 900;
}
.analysis-pill {
  padding: 6rpx 14rpx;
  border-radius: 999rpx;
  background: #eaf4e8;
  color: #4f7f53;
  font-size: 22rpx;
  font-weight: 900;
}
.analysis-desc,
.hint-card {
  display: block;
  margin-top: 10rpx;
  color: #6b7568;
  font-size: 24rpx;
  line-height: 1.6;
}
.hint-card {
  margin-top: 18rpx;
  background: #fff0d9;
  color: #8a541e;
  font-weight: 800;
}
.diet-record {
  padding: 20rpx 0;
  border-bottom: 1rpx solid rgba(139, 154, 137, 0.18);
}
.diet-record:last-child {
  border-bottom: none;
}
.diet-title,
.diet-meta {
  display: block;
}
.diet-title {
  color: #26382a;
  font-size: 27rpx;
  font-weight: 900;
}
.diet-meta {
  margin-top: 8rpx;
  color: #7b8578;
  font-size: 23rpx;
  line-height: 1.5;
}
.submit {
  margin-top: 26rpx;
}
</style>
