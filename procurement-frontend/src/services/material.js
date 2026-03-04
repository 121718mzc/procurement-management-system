// 物料服务
import api from './api';

export const materialService = {
  // 获取物料列表
  getMaterials: (page = 1, perPage = 10) => api.get(`/material/?page=${page}&per_page=${perPage}`),
  
  // 添加物料
  addMaterial: (data) => api.post('/material/', data),
  
  // 更新物料
  updateMaterial: (id, data) => api.put(`/material/${id}`, data),
  
  // 删除物料
  deleteMaterial: (id) => api.delete(`/material/${id}`)
};