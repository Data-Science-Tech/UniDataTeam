import { defineStore } from 'pinia';
import { useStorage } from '@vueuse/core';

export const useGlobalStore = defineStore('global', {
    state: () => ({
        modelConfig: useStorage('modelConfig', {
            algorithm: null,
            learningRate: 0.005,
            numEpochs: 10,
            batchSize: 4,
            momentumValue: 0.9,
            weightDecay: 0.0005,
            sceneIds: [],
            userId: null,
            status: null,
            trainingResults: ''
        }),
        algorithmId: useStorage('algorithmId', 1),
        configId: useStorage('configId', 1),
        resultId: useStorage('resultId', 1),
        serverId: useStorage('serverId', null),
        userId: useStorage('userId', 1)
    }),
    actions: {
        setSharedData(key, value) {
            this.sharedData[key] = value;
        },
        getSharedData(key) {
            return this.sharedData[key];
        },
        setAlgorithmId(id) {
            this.algorithmId = id;
        },
        getAlgorithmId() {
            return this.algorithmId;
        },
        setConfigId(id) {
            this.configId = id;
        },
        getConfigId() {
            return this.configId;
        },
        setResultId(id) {
            this.resultId = id;
        },
        getResultId() {
            return this.resultId;
        },
        setServerId(id) {
            this.serverId = id;
        },
        getServerId() {
            return this.serverId;
        },
        setUserId(id) {
            this.userId = id;
        },
        getUserId() {
            return this.userId;
        },
        resetForm() {
            this.modelConfig = {
                algorithm: null,
                learningRate: 0.005,
                numEpochs: 10,
                batchSize: 4,
                momentumValue: 0.9,
                weightDecay: 0.0005,
                sceneIds: [],
                userId: null,
                status: null,
                trainingResults: ''
            };
            this.algorithmId = 1;
            this.configId = 1;
            this.resultId = 1;
            this.serverId = null;
        },
        clearUserInfo() {
            this.userId = 1;
            this.resetForm();
            localStorage.clear(); // 清除所有本地存储的数据
        }
    }
});
