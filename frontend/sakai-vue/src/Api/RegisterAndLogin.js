import axios from 'axios';
import { API_BASE_URL } from './config';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default {
    // 注册
    register(registerInfo) {
        return apiClient.post('/api/user/register', registerInfo);
    },

    // 登录
    login(loginInfo) {
        return apiClient.post('/api/user/login', loginInfo);
    }
};
