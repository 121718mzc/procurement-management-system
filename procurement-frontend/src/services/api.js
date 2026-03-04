// 基础API配置
import axios from 'axios';
import { ElMessage } from 'element-plus';

const api = axios.create({
  baseURL: 'http://127.0.0.1:5000/',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
api.interceptors.request.use(
  config => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = token;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    // 统一处理错误
    if (error.response) {
      // 服务器返回错误状态码
      const status = error.response.status;
      const message = error.response.data.error || error.response.data.message || '请求失败';
      
      switch (status) {
        case 400:
          ElMessage.error(`请求参数错误: ${message}`);
          break;
        case 401:
          ElMessage.error(`未授权: ${message}`);
          // 可以在这里处理登录过期的逻辑
          break;
        case 403:
          ElMessage.error(`禁止访问: ${message}`);
          break;
        case 404:
          ElMessage.error(`资源不存在: ${message}`);
          break;
        case 500:
          ElMessage.error(`服务器错误: ${message}`);
          break;
        default:
          ElMessage.error(`请求失败: ${message}`);
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      ElMessage.error('网络错误，服务器无响应');
    } else {
      // 请求配置出错
      ElMessage.error(`请求配置错误: ${error.message}`);
    }
    return Promise.reject(error);
  }
);

export default api;
