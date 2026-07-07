<template>
  <text :class="['status-pill', tone]">{{ text }}</text>
</template>

<script setup>
defineProps({
  text: {
    type: String,
    default: '正常'
  },
  tone: {
    type: String,
    default: 'good'
  }
})
</script>

<style scoped>
.status-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42rpx;
  padding: 0 18rpx;
  border-radius: 999rpx;
  background: #eaf7ef;
  color: #2f7d55;
  font-size: 23rpx;
  font-weight: 700;
  white-space: nowrap;
}
.status-pill.warn {
  background: #fff2df;
  color: #b86a19;
}
.status-pill.danger {
  background: #ffe8e3;
  color: #bd4a38;
}
.status-pill.info {
  background: #e8f1ff;
  color: #2f69b8;
}
.status-pill.soft {
  background: #f4efe6;
  color: #8a6741;
}
</style>
