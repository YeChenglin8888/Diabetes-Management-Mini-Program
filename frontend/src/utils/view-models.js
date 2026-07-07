export function glucoseStatusTone(status) {
  if (status === '偏高') return 'warn'
  if (status === '偏低') return 'danger'
  return 'good'
}

export function glucoseStatusText(status) {
  if (status === '偏高') return '偏高，建议复盘饮食与运动'
  if (status === '偏低') return '偏低，注意及时补充碳水'
  if (status === '正常') return '状态平稳，继续保持'
  return '等待你的第一条记录'
}

export function formatDateLabel(value) {
  if (!value) return '--'
  const text = String(value)
  const datePart = text.includes(' ') ? text.split(' ')[0] : text
  return datePart.slice(5).replace('-', '/')
}

export function formatTimeLabel(value) {
  if (!value) return '--:--'
  const text = String(value)
  const timePart = text.includes(' ') ? text.split(' ')[1] : text
  return timePart ? timePart.slice(0, 5) : '--:--'
}

export function buildGlucoseTrend(records = [], limit = 7) {
  const source = [...records].slice(0, limit).reverse()
  return {
    categories: source.map((item) => formatDateLabel(item.measureTime)),
    series: [
      {
        name: '血糖',
        data: source.map((item) => Number(item.glucoseValue || 0))
      }
    ]
  }
}

export function buildCarbChart(report) {
  const total = Number(report?.totalCarb || 0)
  const average = total ? Number((total / 7).toFixed(1)) : 0
  return {
    categories: ['周总量', '日均'],
    series: [
      {
        name: '碳水',
        data: [total, average]
      }
    ]
  }
}

export function recipeTags(recipe = {}) {
  const tags = []
  if (recipe.mealType) tags.push(recipe.mealType)
  const text = `${recipe.recipeName || ''}${recipe.recommendReason || ''}${recipe.ingredients || ''}`
  if (text.includes('低GI') || text.includes('低 GI')) tags.push('低GI')
  if (text.includes('纤维')) tags.push('高纤维')
  if (text.includes('蛋白')) tags.push('优蛋白')
  if (text.includes('清淡')) tags.push('清淡')
  return [...new Set(tags)].slice(0, 4)
}

export function recipeCover(recipe = {}) {
  const meal = recipe.mealType || ''
  if (meal.includes('早餐')) return { icon: '早', tone: 'sunrise' }
  if (meal.includes('午餐')) return { icon: '午', tone: 'leaf' }
  if (meal.includes('晚餐')) return { icon: '晚', tone: 'night' }
  return { icon: '食', tone: 'snack' }
}

export function profileCompletion(user) {
  if (!user) return 0
  const fields = ['username', 'phone', 'gender', 'age', 'diabetesType']
  const done = fields.filter((key) => user[key]).length
  return Math.round((done / fields.length) * 100)
}
