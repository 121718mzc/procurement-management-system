import api from './api'

export const contractService = {
  // 获取合同列表
  getContracts: async (page = 1, pageSize = 10) => {
    try {
      const response = await api.get('/contract/', {
        params: { page, per_page: pageSize }
      })
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 添加合同
  addContract: async (contractData) => {
    try {
      const response = await api.post('/contract/', contractData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 更新合同
  updateContract: async (id, contractData) => {
    try {
      const response = await api.put(`/contract/${id}`, contractData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 删除合同
  deleteContract: async (id) => {
    try {
      const response = await api.delete(`/contract/${id}`)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 导出合同为PDF
  exportContract: async (id) => {
    try {
      const response = await api.get(`/contract/${id}/export`, {
        responseType: 'blob'
      })
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