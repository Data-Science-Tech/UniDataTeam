import axios from 'axios';
import { API_BASE_URL } from './config';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

const GetAllServers = async () => {
  try {
    const response = await apiClient.get('/api/server-types');
    console.log('响应头:', response.headers);
    console.log('响应数据:', response.data);
    if (response.headers['content-type'] !== 'application/json') {
      throw new Error('服务器返回的不是 JSON 数据');
    }
    return response;
  } catch (error) {
    console.error('获取服务器类型失败:', error);
    throw error;
  }
};

export default GetAllServers;
