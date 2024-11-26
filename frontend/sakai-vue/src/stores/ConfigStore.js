import { defineStore } from 'pinia';

export const useGlobalStore = defineStore('global', {
    state: () => ({
        modelConfig: {
            algorithm: 'FAST_R_CNN',
            learningRate: 0.005,
            numEpochs: 10,
            batchSize: 4,
            momentumValue: 0.9,
            weightDecay: 0.0005,
            sceneId: 1,
            modelSavePath: '/path/to/save/model',
            status: 'PENDING',
            trainingResults: ''
        },
        configId: 1,
        resultId: 1,
    }),
    actions: {
        setSharedData(key, value) {
            this.sharedData[key] = value;
        },
        getSharedData(key) {
            return this.sharedData[key];
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
    }
});


