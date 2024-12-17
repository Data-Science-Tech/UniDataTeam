import axios from 'axios';
import { API_BASE_URL } from './config';

const apiClient = axios.create({
  baseURL: API_BASE_URL,  
  headers: {
    'Content-Type': 'application/json'
  }
});

export default {
    // 根据id获取所有热任务
    getalltests(id) {
        return apiClient.get(`/api/task_management/get_user_server_usage_by_userid/${userId}`);
      }
  };

