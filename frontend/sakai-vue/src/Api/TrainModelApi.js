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
    return apiClient.post('/api/configuration/create_config', modelConfig);
  },

  // 使用创建的配置训练模型
  startTraining(id, serverId, taskName) {
    console.log('startTraining', id, serverId, taskName);
    return apiClient.post(`/api/configuration/train/${id}`, {
      serverId: serverId,
      taskName: taskName
    });
  },
  // 获取所有场景id和对应的描述
  getallscene() {
    return apiClient.get(`/api/sceneinfo/all`);
  }
};

