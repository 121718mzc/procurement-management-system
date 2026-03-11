import api from './api'

export const pricingService = {
  // 获取价格列表
  getPricings: async (page = 1, pageSize = 10) => {
    try {
      const response = await api.get('/pricing/', {
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
      const response = await api.post('/pricing/', pricingData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 更新价格
  updatePricing: async (id, pricingData) => {
    try {
      const response = await api.put(`/pricing/${id}`, pricingData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 删除价格
  deletePricing: async (id) => {
    try {
      const response = await api.delete(`/pricing/${id}`)
      return response
    } catch (error) {
      throw error
    }
  },

  // 获取物料列表
  getMaterials: async () => {
    try {
      const response = await api.get('/material/')
      return response
    } catch (error) {
      throw error
    }
  },

  // 获取供应商列表
  getSuppliers: async () => {
    try {
      const response = await api.get('/supplier/')
      return response
    } catch (error) {
      throw error
    }
  }
}