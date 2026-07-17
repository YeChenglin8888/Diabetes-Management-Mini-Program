<template>
  <view class="page">
    <view class="profile-hero" v-if="user">
      <view class="avatar">{{ avatarText }}</view>
      <view class="profile-main">
        <text class="profile-name">{{ user.username }}</text>
        <text class="profile-sub">{{ user.diabetesType || '未填写糖尿病类型' }}</text>
      </view>
      <StatusPill :text="`${completion}% 完成`" tone="soft" />
    </view>

    <view class="metric-grid section" v-if="user">
      <HealthMetricCard label="年龄" :value="user.age || '--'" unit="岁" hint="健康档案信息" icon="龄" tone="green" />
      <HealthMetricCard label="手机号" :value="user.phone ? '已填' : '--'" hint="用于账号识别" icon="号" tone="blue" />
    </view>

    <view class="panel section" v-if="user">
      <WarmSectionHeader title="健康档案" desc="课程原型中仅展示基础信息，后续可扩展目标血糖和用药提醒。" />
      <view class="info-row"><text>用户名</text><text>{{ user.username }}</text></view>
      <view class="info-row"><text>手机号</text><text>{{ user.phone || '--' }}</text></view>
      <view class="info-row"><text>性别</text><text>{{ user.gender || '--' }}</text></view>
      <view class="info-row"><text>年龄</text><text>{{ user.age || '--' }}</text></view>
      <view class="info-row"><text>糖尿病类型</text><text>{{ user.diabetesType || '--' }}</text></view>
    </view>

    <view class="panel">
      <WarmSectionHeader title="常用功能" desc="需要灵感或重新登录时，从这里走。" />
      <wd-button plain block @click="goRecipes">查看降糖食谱</wd-button>
      <view class="gap"></view>
      <wd-button type="error" block @click="logout">退出登录</wd-button>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { clearCurrentUser, getCurrentUser } from '../../utils/request'
import { profileCompletion } from '../../utils/view-models'

const user = ref(null)
const completion = computed(() => profileCompletion(user.value))
const avatarText = computed(() => (user.value?.username || '糖').slice(0, 1).toUpperCase())

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
.profile-hero {
  display: flex;
  align-items: center;
  gap: 20rpx;
  margin-bottom: 24rpx;
  padding: 34rpx;
  border-radius: 38rpx;
  background: linear-gradient(135deg, #e9f4e6, #fff1da);
  box-shadow: 0 20rpx 54rpx rgba(104, 109, 76, 0.12);
}
.avatar {
  width: 104rpx;
  height: 104rpx;
  flex: 0 0 auto;
  border-radius: 34rpx;
  background: #5c8f5f;
  color: #ffffff;
  text-align: center;
  line-height: 104rpx;
  font-size: 42rpx;
  font-weight: 900;
}
.profile-main {
  flex: 1;
  min-width: 0;
}
.profile-name {
  display: block;
  color: #253528;
  font-size: 38rpx;
  font-weight: 900;
}
.profile-sub {
  display: block;
  margin-top: 6rpx;
  color: #778276;
  font-size: 25rpx;
}
.metric-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}
.info-row {
  display: flex;
  justify-content: space-between;
  gap: 18rpx;
  padding: 20rpx 0;
  border-bottom: 1rpx solid rgba(139, 154, 137, 0.18);
  color: #4d5d4c;
  font-size: 28rpx;
}
.info-row text:last-child {
  color: #253528;
  font-weight: 800;
}
.info-row:last-child {
  border-bottom: none;
}
.gap {
  height: 18rpx;
}
</style>
