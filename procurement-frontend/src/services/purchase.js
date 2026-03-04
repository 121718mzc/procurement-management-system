// 采购订单服务
import api from './api';

export const purchaseService = {
  // 获取采购订单列表
  getPurchaseOrders: (params) => api.get('/purchase/', { params }),
  
  // 添加采购订单
  addPurchaseOrder: (data) => api.post('/purchase/', data),
  
  // 更新采购订单
  updatePurchaseOrder: (id, data) => api.put(`/purchase/${id}`, data),
  
  // 删除采购订单
  deletePurchaseOrder: (id) => api.delete(`/purchase/${id}`),
  
  // 获取采购订单详情
  getPurchaseOrderDetail: (id) => api.get(`/purchase/${id}`)
};
