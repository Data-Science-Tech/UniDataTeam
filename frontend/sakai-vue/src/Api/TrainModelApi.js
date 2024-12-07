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
  createModelConfig(modelConfig) {
    return apiClient.post('/api/model-configs', modelConfig);
  },

  // 使用创建的配置训练模型
  startTraining(id) {
    return apiClient.post(`/api/model-configs/${id}/train`);
  },
  // 获取所有场景id和对应的描述
  getallscene() {
    return apiClient.get(`api/scene-info/all`);
  }
};

