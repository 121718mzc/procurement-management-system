import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

export const contractService = {
  // 获取合同列表
  getContracts: async (page = 1, pageSize = 10) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/contract/`, {
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
      const response = await axios.post(`${API_BASE_URL}/contract/`, contractData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 更新合同
  updateContract: async (id, contractData) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/contract/${id}`, contractData)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 删除合同
  deleteContract: async (id) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/contract/${id}`)
      return response
    } catch (error) {
      throw error
    }
  },
  
  // 导出合同为PDF
  exportContract: async (id) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/contract/${id}/export`, {
        responseType: 'blob'
      })
      return response
    } catch (error) {
      throw error
    }
  }
}