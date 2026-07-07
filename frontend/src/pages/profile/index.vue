<template>
  <view class="page">
    <view class="section">
      <text class="title">个人中心</text>
      <text class="subtle">查看当前登录患者信息。</text>
    </view>

    <view class="panel section" v-if="user">
      <view class="info-row"><text>用户名</text><text>{{ user.username }}</text></view>
      <view class="info-row"><text>手机号</text><text>{{ user.phone || '--' }}</text></view>
      <view class="info-row"><text>性别</text><text>{{ user.gender || '--' }}</text></view>
      <view class="info-row"><text>年龄</text><text>{{ user.age || '--' }}</text></view>
      <view class="info-row"><text>糖尿病类型</text><text>{{ user.diabetesType || '--' }}</text></view>
    </view>

    <view class="panel">
      <wd-button plain block @click="goRecipes">查看降糖食谱</wd-button>
      <view class="gap"></view>
      <wd-button type="error" block @click="logout">退出登录</wd-button>
    </view>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { clearCurrentUser, getCurrentUser } from '../../utils/request'

const user = ref(null)

onShow(() => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
  }
})

function goRecipes() {
  uni.navigateTo({ url: '/pages/recipes/index' })
}

function logout() {
  clearCurrentUser()
  uni.redirectTo({ url: '/pages/auth/login' })
}
</script>

<style scoped>
.info-row {
  display: flex;
  justify-content: space-between;
  gap: 18rpx;
  padding: 18rpx 0;
  border-bottom: 1rpx solid #eaecf0;
  color: #344054;
  font-size: 28rpx;
}
.info-row:last-child {
  border-bottom: none;
}
.gap {
  height: 18rpx;
}
</style>
