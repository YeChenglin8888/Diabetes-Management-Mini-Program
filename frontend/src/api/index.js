import { request } from '../utils/request'

export const api = {
  health: () => request('/health'),
  register: (data) => request('/auth/register', { method: 'POST', data }),
  login: (data) => request('/auth/login', { method: 'POST', data }),
  listGlucose: (params) => request(`/glucose?${toQuery(params)}`),
  createGlucose: (data) => request('/glucose', { method: 'POST', data }),
  listFoods: (params = {}) => request(`/foods?${toQuery(params)}`),
  calculateDiet: (data) => request('/diets/calculate', { method: 'POST', data }),
  saveDiet: (data) => request('/diets', { method: 'POST', data }),
  listRecipes: (params = {}) => request(`/recipes?${toQuery(params)}`),
  getRecipe: (recipeId) => request(`/recipes/${recipeId}`),
  getWeeklyReport: (params) => request(`/reports/weekly?${toQuery(params)}`)
}

function toQuery(params = {}) {
  return Object.entries(params)
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
    .join('&')
}
