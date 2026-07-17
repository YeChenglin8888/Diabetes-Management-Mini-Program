<template>
  <view class="page auth-page">
    <view class="hero">
      <view class="hero-badge">控糖日常 · 温柔一点</view>
      <text class="hero-title">把血糖、饮食和每周变化放在同一个小本子里</text>
      <text class="hero-copy">记录不用复杂，关键是每天都能看懂自己。今天从一条血糖或一顿饭开始。</text>
      <view class="hero-pills">
        <text>血糖趋势</text>
        <text>碳水测算</text>
        <text>降糖食谱</text>
      </view>
    </view>

    <view class="panel auth-card">
      <view class="tabs">
        <text :class="['tab', mode === 'login' ? 'active' : '']" @tap="mode = 'login'">登录</text>
        <text :class="['tab', mode === 'register' ? 'active' : '']" @tap="mode = 'register'">注册</text>
      </view>

      <view class="field">
        <text class="label">用户名</text>
        <input class="input" v-model="form.username" placeholder="请输入用户名或手机号" />
      </view>
      <view class="field">
        <text class="label">密码</text>
        <input class="input" v-model="form.password" password placeholder="请输入密码" />
      </view>

      <template v-if="mode === 'register'">
        <view class="field">
          <text class="label">手机号</text>
          <input class="input" v-model="form.phone" placeholder="请输入手机号" />
        </view>
        <view class="row field">
          <view class="grow">
            <text class="label">性别</text>
            <picker :range="genders" @change="form.gender = genders[$event.detail.value]">
              <view class="picker">{{ form.gender || '请选择性别' }}</view>
            </picker>
          </view>
          <view class="grow">
            <text class="label">年龄</text>
            <input class="input" v-model.number="form.age" type="number" placeholder="年龄" />
          </view>
        </view>
        <view class="field">
          <text class="label">糖尿病类型</text>
          <picker :range="types" @change="form.diabetesType = types[$event.detail.value]">
            <view class="picker">{{ form.diabetesType || '请选择类型' }}</view>
          </picker>
        </view>
      </template>

      <view class="submit">
        <wd-button type="primary" block @click="submit">
          {{ mode === 'login' ? '进入今日看板' : '注册并进入' }}
        </wd-button>
      </view>
      <view class="demo-box" @tap="useDemo">
        <text class="demo-title">使用演示账号</text>
        <text class="demo-text">demo_patient / 123456</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { api } from '../../api'
import { setCurrentUser } from '../../utils/request'

const mode = ref('login')
const genders = ['女', '男', '其他']
const types = ['1型糖尿病', '2型糖尿病', '妊娠糖尿病', '其他']
const form = reactive({
  username: 'demo_patient',
  password: '123456',
  phone: '',
  gender: '',
  age: '',
  diabetesType: ''
})

function useDemo() {
  mode.value = 'login'
  form.username = 'demo_patient'
  form.password = '123456'
  uni.showToast({ title: '已填入演示账号', icon: 'none' })
}

async function submit() {
  if (!form.username || !form.password) {
    uni.showToast({ title: '请填写用户名和密码', icon: 'none' })
    return
  }
  if (mode.value === 'register') {
    await api.register({ ...form })
  }
  const user = await api.login({ username: form.username, password: form.password })
  setCurrentUser(user)
  uni.switchTab({ url: '/pages/home/index' })
}
</script>

<style scoped>
.auth-page {
  padding-top: 72rpx;
}
.hero {
  position: relative;
  overflow: hidden;
  box-sizing: border-box;
  min-height: 430rpx;
  margin-bottom: 28rpx;
  padding: 42rpx 34rpx;
  border-radius: 42rpx;
  background:
    linear-gradient(135deg, rgba(255, 246, 230, 0.96), rgba(229, 242, 225, 0.92)),
    radial-gradient(circle at 86% 18%, rgba(225, 135, 55, 0.28), transparent 30%);
  box-shadow: 0 22rpx 58rpx rgba(121, 104, 72, 0.12);
}
.hero::after {
  position: absolute;
  right: -46rpx;
  bottom: -34rpx;
  width: 230rpx;
  height: 230rpx;
  border: 28rpx solid rgba(118, 151, 103, 0.18);
  border-radius: 50%;
  content: '';
}
.hero-badge {
  display: inline-flex;
  padding: 10rpx 18rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.72);
  color: #b86a19;
  font-size: 23rpx;
  font-weight: 900;
}
.hero-title {
  display: block;
  margin-top: 26rpx;
  max-width: 600rpx;
  color: #26382a;
  font-size: 46rpx;
  font-weight: 900;
  line-height: 1.22;
}
.hero-copy {
  display: block;
  margin-top: 18rpx;
  max-width: 560rpx;
  color: #687664;
  font-size: 27rpx;
  line-height: 1.65;
}
.hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 14rpx;
  margin-top: 28rpx;
}
.hero-pills text {
  padding: 10rpx 16rpx;
  border-radius: 999rpx;
  background: rgba(255, 255, 255, 0.74);
  color: #557956;
  font-size: 23rpx;
  font-weight: 800;
}
.auth-card {
  padding: 32rpx;
}
.tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16rpx;
  margin-bottom: 18rpx;
  padding: 8rpx;
  border-radius: 24rpx;
  background: #f4efe6;
}
.tab {
  height: 72rpx;
  border-radius: 18rpx;
  color: #7a836f;
  text-align: center;
  line-height: 72rpx;
  font-size: 28rpx;
  font-weight: 800;
}
.tab.active {
  background: #ffffff;
  color: #4f7f53;
  box-shadow: 0 10rpx 26rpx rgba(88, 105, 76, 0.1);
}
.submit {
  margin-top: 32rpx;
}
.demo-box {
  margin-top: 22rpx;
  padding: 20rpx;
  border-radius: 22rpx;
  background: #fff6e8;
  text-align: center;
}
.demo-title {
  display: block;
  color: #8a6741;
  font-size: 24rpx;
  font-weight: 900;
}
.demo-text {
  display: block;
  margin-top: 4rpx;
  color: #c97827;
  font-size: 25rpx;
  font-weight: 800;
}
</style>
