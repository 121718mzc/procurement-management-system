// 用户服务
import api from './api';

export const userService = {
  // 用户登录
  login: (data) => api.post('/user/login', data),
  
  // 获取用户信息
  getUserInfo: () => api.get('/user/info')
};
