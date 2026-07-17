const BASE_URL = 'http://10.43.55.13:8000/api'

export function getCurrentUser() {
  return uni.getStorageSync('currentUser') || null
}

export function setCurrentUser(user) {
  uni.setStorageSync('currentUser', user)
}

export function clearCurrentUser() {
  uni.removeStorageSync('currentUser')
}

export function request(path, options = {}) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${BASE_URL}${path}`,
      method: options.method || 'GET',
      data: options.data || {},
      header: {
        'content-type': 'application/json'
      },
      success(res) {
        const body = res.data || {}
        if (body.code === 200) {
          resolve(body.data)
          return
        }
        const message = body.message || '请求失败'
        uni.showToast({ title: message, icon: 'none' })
        reject(new Error(message))
      },
      fail(err) {
        uni.showToast({ title: '无法连接后端服务', icon: 'none' })
        reject(err)
      }
    })
  })
}
