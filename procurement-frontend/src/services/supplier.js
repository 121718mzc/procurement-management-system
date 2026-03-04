// 供应商服务
import api from './api';

export const supplierService = {
  // 获取供应商列表
  getSuppliers: (page = 1, perPage = 10) => api.get(`/supplier/?page=${page}&per_page=${perPage}`),
  
  // 添加供应商
  addSupplier: (data) => api.post('/supplier/', data),
  
  // 更新供应商
  updateSupplier: (id, data) => api.put(`/supplier/${id}`, data),
  
  // 删除供应商
  deleteSupplier: (id) => api.delete(`/supplier/${id}`)
};
