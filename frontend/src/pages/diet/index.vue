<template>
  <view class="page">
    <view class="section">
      <text class="title">饮食测算</text>
      <text class="subtle">选择食物和重量，自动估算本餐碳水。</text>
    </view>

    <view class="panel section">
      <view class="field">
        <text class="label">餐次</text>
        <picker :range="mealTypes" @change="form.mealType = mealTypes[$event.detail.value]">
          <view class="picker">{{ form.mealType }}</view>
        </picker>
      </view>
      <view class="field">
        <text class="label">选择食物</text>
        <picker :range="foods" range-key="foodName" @change="pickFood">
          <view class="picker">{{ selectedFood ? selectedFood.foodName : '请选择食物' }}</view>
        </picker>
      </view>
      <view class="row field">
        <view class="grow">
          <text class="label">重量 g</text>
          <input class="input" v-model.number="weightG" type="digit" placeholder="例如 100" />
        </view>
        <view class="add-btn">
          <wd-button type="primary" @click="addItem">添加</wd-button>
        </view>
      </view>
    </view>

    <view class="panel section">
      <text class="block-title">本餐明细</text>
      <view v-if="items.length === 0" class="subtle">请至少添加一种食物。</view>
      <view class="item" v-for="(item, index) in items" :key="index">
        <view>
          <text class="item-name">{{ item.foodName }}</text>
          <text class="subtle">{{ item.weightG }}g · {{ item.carbValue }}g 碳水</text>
        </view>
        <text class="remove" @tap="items.splice(index, 1)">删除</text>
      </view>
      <view class="total">总碳水：{{ totalCarb }}g</view>
      <wd-button type="success" block @click="saveDiet">保存饮食记录</wd-button>
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
const selectedFood = ref(null)
const weightG = ref('')
const user = ref(null)
const form = reactive({ mealType: '早餐' })
const totalCarb = computed(() => items.value.reduce((sum, item) => sum + Number(item.carbValue), 0).toFixed(2))

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  foods.value = await api.listFoods()
})

function pickFood(event) {
  selectedFood.value = foods.value[event.detail.value]
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
}
</script>

<style scoped>
.add-btn {
  padding-top: 50rpx;
}
.block-title {
  display: block;
  margin-bottom: 18rpx;
  font-size: 30rpx;
  font-weight: 700;
}
.item {
  display: flex;
  justify-content: space-between;
  gap: 16rpx;
  padding: 18rpx 0;
  border-bottom: 1rpx solid #eaecf0;
}
.item-name {
  display: block;
  margin-bottom: 8rpx;
  font-weight: 700;
}
.remove {
  color: #b42318;
  font-size: 26rpx;
}
.total {
  margin: 22rpx 0;
  color: #0f766e;
  font-size: 34rpx;
  font-weight: 800;
}
</style>
