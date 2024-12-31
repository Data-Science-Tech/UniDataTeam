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
  downloadModel(trainingResultId) {
    return apiClient.get(`/api/task_management/download_model_by_training_result_id/${trainingResultId}`);
  },
};
