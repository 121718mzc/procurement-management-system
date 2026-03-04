import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

export const pricingService = {
  // 获取价格列表
  getPricings: async (page = 1, pageSize = 10) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/pricing/`, {
        params: { page, per_page: pageSize }
      })
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 添加价格
  addPricing: async (pricingData) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/pricing/`, pricingData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 更新价格
  updatePricing: async (id, pricingData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/pricing/${id}`, pricingData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 删除价格
  deletePricing: async (id) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/pricing/${id}`)
      return response
    } catch (error) {
      throw error
    }
  }
}