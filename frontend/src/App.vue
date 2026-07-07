<script>
export default {
  onLaunch() {
    console.log('diabetes miniapp launched')
  }
}
</script>

<style>
page {
  min-height: 100%;
  background: #fff8ed;
  color: #253528;
  font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif;
}

.page {
  min-height: 100vh;
  box-sizing: border-box;
  padding: 28rpx;
  background:
    radial-gradient(circle at 8% 4%, rgba(232, 154, 70, 0.18), transparent 34%),
    radial-gradient(circle at 92% 8%, rgba(106, 151, 103, 0.14), transparent 30%),
    linear-gradient(180deg, #fff8ed 0%, #f7f1e7 48%, #eef5ec 100%);
}

.section {
  margin-bottom: 24rpx;
}

.panel {
  box-sizing: border-box;
  padding: 28rpx;
  border: 1rpx solid rgba(98, 122, 91, 0.1);
  border-radius: 28rpx;
  background: rgba(255, 255, 255, 0.88);
  box-shadow: 0 18rpx 48rpx rgba(92, 102, 75, 0.1);
}

.title {
  display: block;
  color: #253528;
  font-size: 42rpx;
  font-weight: 900;
  line-height: 1.25;
}

.subtle {
  color: #778276;
  font-size: 26rpx;
  line-height: 1.6;
}

.field {
  margin-top: 20rpx;
}

.label {
  display: block;
  margin-bottom: 10rpx;
  color: #4d5d4c;
  font-size: 26rpx;
  font-weight: 800;
}

.input,
.picker {
  box-sizing: border-box;
  width: 100%;
  min-height: 84rpx;
  padding: 0 22rpx;
  border: 1rpx solid rgba(117, 135, 111, 0.22);
  border-radius: 20rpx;
  background: #fffdf8;
  color: #253528;
  font-size: 28rpx;
  line-height: 84rpx;
}

.row {
  display: flex;
  gap: 18rpx;
  align-items: center;
}

.row > .grow {
  flex: 1;
  min-width: 0;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.status {
  display: inline-flex;
  padding: 7rpx 18rpx;
  border-radius: 999rpx;
  background: #eaf7ef;
  color: #2f7d55;
  font-size: 24rpx;
  font-weight: 800;
}

.status.warn {
  background: #fff2df;
  color: #b86a19;
}

.status.danger {
  background: #ffe8e3;
  color: #bd4a38;
}

.warm-card {
  border-radius: 32rpx;
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.94), rgba(255, 247, 234, 0.9));
}

.soft-button-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18rpx;
}

.page-note {
  color: #8a6741;
  font-size: 24rpx;
  line-height: 1.55;
}
</style>
