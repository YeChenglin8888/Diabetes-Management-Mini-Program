<template>
  <view class="page auth-page">
    <view class="hero">
      <text class="title">糖尿病饮食血糖管理</text>
      <text class="subtle">记录血糖、测算碳水、查看食谱与每周趋势。</text>
    </view>

    <view class="panel">
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
          {{ mode === 'login' ? '登录' : '注册并登录' }}
        </wd-button>
      </view>
      <text class="demo subtle">演示账号：demo_patient / 123456</text>
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
  padding-top: 86rpx;
}
.hero {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 42rpx;
}
.tabs {
  display: flex;
  gap: 18rpx;
  margin-bottom: 18rpx;
}
.tab {
  flex: 1;
  height: 72rpx;
  border-radius: 12rpx;
  background: #f2f4f7;
  color: #667085;
  text-align: center;
  line-height: 72rpx;
  font-size: 28rpx;
}
.tab.active {
  background: #d9f5ef;
  color: #0f766e;
  font-weight: 700;
}
.submit {
  margin-top: 30rpx;
}
.demo {
  display: block;
  margin-top: 18rpx;
  text-align: center;
}
</style>
