import axios from 'axios';
import { API_BASE_URL } from './config';

const apiClient = axios.create({
  baseURL: API_BASE_URL,  
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
  // 创建模型配置
  getTrainingResults(taskId) {
    return apiClient.get(`/api/training-results/by-config/${taskId}`);
  },
};

