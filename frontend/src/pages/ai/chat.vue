<template>
  <view class="page chat-page">
    <WarmSectionHeader
      eyebrow="AI CHAT"
      title="AI 对话"
      desc="结合你的健康档案和近 7 天统计，回答饮食、记录和趋势复盘问题。"
    />

    <view class="panel status-panel section">
      <view>
        <text class="service-title">{{ aiConfig?.configured ? 'AI 服务已配置' : 'AI 服务未配置' }}</text>
        <text class="subtle">{{ aiConfig?.configured ? `模型：${aiConfig.model || 'deepseek-v4-pro'}` : '请先在后端 .env 配置 AI_API_KEY' }}</text>
      </view>
      <wd-button size="small" plain @click="loadAiConfig">检测</wd-button>
    </view>

    <scroll-view class="chat-list section" scroll-y :scroll-into-view="lastMessageId">
      <view
        v-for="(item, index) in messages"
        :id="`msg-${index}`"
        :key="index"
        class="message-row"
        :class="item.role"
      >
        <view class="bubble">
          <text class="bubble-text">{{ item.content }}</text>
        </view>
      </view>
    </scroll-view>

    <view class="quick-questions section">
      <text class="chip" @tap="fillQuestion('我最近一周血糖有什么需要注意？')">本周血糖</text>
      <text class="chip" @tap="fillQuestion('我下一餐主食应该怎么控制？')">下一餐建议</text>
      <text class="chip" @tap="fillQuestion('快碳偏多时可以怎么替换？')">快碳替换</text>
    </view>

    <view class="input-panel">
      <input
        class="chat-input"
        v-model="question"
        confirm-type="send"
        placeholder="输入你的问题"
        @confirm="sendQuestion"
      />
      <wd-button type="primary" :loading="sending" @click="sendQuestion">发送</wd-button>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { api } from '../../api'
import { getCurrentUser } from '../../utils/request'

const user = ref(null)
const aiConfig = ref(null)
const question = ref('')
const sending = ref(false)
const messages = ref([
  {
    role: 'assistant',
    content: '你好，我会结合你的近 7 天血糖和饮食统计来回答。可以问我“这周哪里需要注意”或“下一餐怎么搭配”。'
  }
])
const lastMessageId = computed(() => `msg-${Math.max(messages.value.length - 1, 0)}`)

onShow(async () => {
  user.value = getCurrentUser()
  if (!user.value) {
    uni.redirectTo({ url: '/pages/auth/login' })
    return
  }
  await loadAiConfig()
})

async function loadAiConfig() {
  try {
    aiConfig.value = await api.getAiConfig()
  } catch {
    aiConfig.value = null
  }
}

function fillQuestion(text) {
  question.value = text
}

async function sendQuestion() {
  const text = question.value.trim()
  if (!text || sending.value) return
  question.value = ''
  messages.value.push({ role: 'user', content: text })
  sending.value = true
  try {
    const result = await api.chatWithAi({
      userId: user.value.userId,
      question: text,
      history: messages.value.slice(-8)
    })
    messages.value.push({
      role: 'assistant',
      content: result.answer || '暂时没有生成回答，请稍后再试。'
    })
    if (result.fallback && result.error) {
      uni.showToast({ title: result.error, icon: 'none' })
    }
  } catch {
    messages.value.push({
      role: 'assistant',
      content: 'AI 对话暂时不可用，请检查后端服务和 AI 配置。'
    })
  } finally {
    sending.value = false
  }
}
</script>

<style scoped>
.chat-page {
  padding-bottom: 140rpx;
}
.status-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18rpx;
}
.service-title {
  display: block;
  color: #253528;
  font-size: 29rpx;
  font-weight: 900;
}
.chat-list {
  height: 720rpx;
}
.message-row {
  display: flex;
  margin-bottom: 18rpx;
}
.message-row.user {
  justify-content: flex-end;
}
.message-row.assistant {
  justify-content: flex-start;
}
.bubble {
  max-width: 78%;
  box-sizing: border-box;
  padding: 20rpx 24rpx;
  border-radius: 26rpx;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 12rpx 32rpx rgba(92, 102, 75, 0.08);
}
.message-row.user .bubble {
  background: #5c8f5f;
  color: #ffffff;
}
.bubble-text {
  font-size: 27rpx;
  line-height: 1.65;
  white-space: pre-wrap;
}
.quick-questions {
  display: flex;
  flex-wrap: wrap;
  gap: 14rpx;
}
.chip {
  padding: 14rpx 20rpx;
  border-radius: 999rpx;
  background: #edf5ec;
  color: #4f7f53;
  font-size: 24rpx;
  font-weight: 800;
}
.input-panel {
  position: fixed;
  right: 28rpx;
  bottom: 28rpx;
  left: 28rpx;
  display: flex;
  gap: 14rpx;
  align-items: center;
  box-sizing: border-box;
  padding: 18rpx;
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 14rpx 44rpx rgba(92, 102, 75, 0.16);
}
.chat-input {
  flex: 1;
  min-width: 0;
  height: 78rpx;
  box-sizing: border-box;
  padding: 0 22rpx;
  border: 1rpx solid rgba(117, 135, 111, 0.22);
  border-radius: 20rpx;
  background: #fffdf8;
  color: #253528;
  font-size: 28rpx;
}
</style>
