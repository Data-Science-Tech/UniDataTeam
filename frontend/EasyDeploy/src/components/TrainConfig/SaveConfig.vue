<template>
    <div>
        <h2>Create Model Config</h2>
        <!-- 表单输入字段 -->
        <form @submit.prevent="createModelConfig">
            <label>
                Algorithm:
                <select v-model="modelConfig.algorithm">
                    <option value="FAST_R_CNN">FAST_R_CNN</option>
                    <option value="SSD">SSD</option>
                </select>
            </label>

            <label>
                Learning Rate:
                <input type="number" v-model="modelConfig.learningRate" step="0.005" />
            </label>

            <label>
                Number of Epochs:
                <input type="number" v-model="modelConfig.numEpochs" />
            </label>

            <label>
                Batch Size:
                <input type="number" v-model="modelConfig.batchSize" />
            </label>

            <label>
                Momentum Value:
                <input type="number" v-model="modelConfig.momentumValue" step="0.1" />
            </label>

            <label>
                Weight Decay:
                <input type="number" v-model="modelConfig.weightDecay" step="0.0001" />
            </label>

            <label>
                Scene ID:
                <input type="number" v-model="modelConfig.sceneId" />
            </label>

            <label>
                Model Save Path:
                <input type="text" v-model="modelConfig.modelSavePath" />
            </label>

            <button type="button" @click="createModelConfig">Create Config</button>
            <button type="button" @click="startTraining">Start Train</button>
        </form>

        <!-- 显示操作状态 -->
        <div v-if="responseMessage">
            <p>{{ responseMessage }}</p>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';
import TrainModelApi from '@/Api/TrainModelApi';

export default {
    name: 'CreateModelConfig',
    setup() {
        const configId = ref(1)
        const modelConfig = ref({
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
        });
        const responseMessage = ref('');

        // 创建模型配置
        // 返回配置id用于训练模型
        const createModelConfig = async () => {
            try {
                console.log(modelConfig.value);
                const response = await TrainModelApi.createModelConfig(modelConfig.value);
                responseMessage.value = '模型参数配置成功!';
                console.log("模型参数配置创建成功:", response.data);
                configId.value = response.data.id;
            } catch (error) {
                responseMessage.value = '创建模型配置失败.';
                console.error("创建模型配置失败:", error);
            }
        };

        // 根据返回配置的id 或者 后续添加选择配置的功能选择对应id的配置
        // 训练模型
        const startTraining = async () => {
            try {
                console.log(configId.value)
                const response = await TrainModelApi.startTraining(configId.value);
                responseMessage.value = '模型开始训练成功!';
                console.log("模型开始训练成功:", response.data);
                configId.value = response.data.id;
            } catch (error) {
                responseMessage.value = '模型训练失败.';
                console.error("模型训练失败:", error);
            }
        };

        return {
            modelConfig,
            responseMessage,
            configId,
            createModelConfig,
            startTraining,
        };
    }
};
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    gap: 1em;
}

label {
    display: flex;
    flex-direction: column;
}

button {
    width: fit-content;
    padding: 0.5em 1em;
}
</style>