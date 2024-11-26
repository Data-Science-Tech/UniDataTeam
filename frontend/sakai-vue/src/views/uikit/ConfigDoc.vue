<template>
    <div class="container">
        <h2>算法选择和模型参数配置</h2>
        <!-- 表单输入字段 -->
        <form @submit.prevent="createModelConfig" class="form-container">
            <div class="form-group">
                <label for="algorithm">算法(Algorithm):</label>
                <select v-model="globalStore.modelConfig.algorithm" id="algorithm" class="input-field">
                    <option v-for="algorithm in algorithms" :key="algorithm" :value="algorithm">{{ algorithm }}</option>
                </select>
            </div>

            <div class="form-group">
                <label for="learningRate">学习率(Learning Rate):</label>
                <input type="number" v-model="globalStore.modelConfig.learningRate" id="learningRate" class="input-field"
                    step="0.005" />
            </div>

            <div class="form-group">
                <label for="numEpochs">迭代次数(Number of Epochs):</label>
                <input type="number" v-model="globalStore.modelConfig.numEpochs" id="numEpochs" class="input-field" />
            </div>

            <div class="form-group">
                <label for="batchSize">样本数量(Batch Size):</label>
                <input type="number" v-model="globalStore.modelConfig.batchSize" id="batchSize" class="input-field" />
            </div>

            <div class="form-group">
                <label for="momentumValue">动量值(Momentum Value):</label>
                <input type="number" v-model="globalStore.modelConfig.momentumValue" id="momentumValue" class="input-field"
                    step="0.1" />
            </div>

            <div class="form-group">
                <label for="weightDecay">权重衰退(Weight Decay):</label>
                <input type="number" v-model="globalStore.modelConfig.weightDecay" id="weightDecay" class="input-field"
                    step="0.0001" />
            </div>

            <div class="form-group">
                <label for="sceneId">场景ID及描述:</label>
                <select v-model="globalStore.modelConfig.sceneId" id="sceneId" class="input-field">
                    <option v-for="scene in scenes" :key="scene.sceneId" :value="scene.sceneId">
                        {{ scene.sceneId }} - {{ scene.sceneDescription }}
                    </option>
                </select>
            </div>

            <div class="button-group">
                <button type="button" @click="createModelConfig" class="button create-btn">创建参数配置</button>
            </div>
        </form>

        <!-- 显示操作状态 -->
        <div v-if="responseMessage" class="response-message">
            <p>{{ responseMessage }}</p>
        </div>
    </div>
</template>

<script setup>
import { ref ,onMounted } from 'vue';
import TrainModelApi from '@/Api/TrainModelApi';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';

// 初始化 Pinia Store
const globalStore = useGlobalStore();
const router = useRouter();

// 本地状态
const scenes = ref([]); // 场景数据
const algorithms = ref(['FAST_R_CNN', 'SSD']);// 后续可以向后端发送代码查询所有存在的算法，完成赋值。
const responseMessage = ref('');

// 创建模型配置
const createModelConfig = async () => {
    try {
        console.log(globalStore.modelConfig);
        const response = await TrainModelApi.createModelConfig(globalStore.modelConfig);
        responseMessage.value = '模型参数配置成功!';
        console.log("模型参数配置创建成功:", response.data);
        globalStore.setConfigId(response.data.id);
        router.push('/uikit/implement');
    } catch (error) {
        responseMessage.value = '创建模型配置失败.';
        console.error("创建模型配置失败:", error);
    }
};

// 获取场景数据
const getallscene = async () => {
    try {
        const response = await TrainModelApi.getallscene();
        scenes.value = response.data;
        console.log('场景数据获取成功:', scenes.value);
    } catch (error) {
        console.error('获取场景数据失败:', error);
    }
};

// 组件挂载时获取场景数据
onMounted(getallscene);
</script>


<style scoped>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Arial', sans-serif;
    background-color: #f9f9f9;
    color: #333;
}

.container {
    max-width: 600px;
    margin: 20px auto;
    padding: 20px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}


.form-container {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 5px;
}

.label {
    font-size: 16px;
    font-weight: bold;
}

.input-field {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.input-field:focus {
    border-color: #007bff;
    outline: none;
}

.button-group {
    display: flex;
    justify-content: center; 
    align-items: center; 
}

.button {
    padding: 10px 20px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.create-btn {
    background-color: #28a745;
    color: white;
}

.create-btn:hover {
    background-color: #218838;
}

.train-btn {
    background-color: #007bff;
    color: white;
}

.train-btn:hover {
    background-color: #0056b3;
}

.response-message {
    margin-top: 20px;
    padding: 10px;
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 4px;
}
</style>