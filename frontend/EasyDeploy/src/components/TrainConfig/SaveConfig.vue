<template>
    <div class="container">
      <h2>Create Model Config</h2>
      <!-- 表单输入字段 -->
      <form @submit.prevent="createModelConfig" class="form-container">
        <div class="form-group">
          <label for="algorithm">Algorithm:</label>
          <select v-model="modelConfig.algorithm" id="algorithm" class="input-field">
            <option value="FAST_R_CNN">FAST_R_CNN</option>
            <option value="SSD">SSD</option>
          </select>
        </div>
  
        <div class="form-group">
          <label for="learningRate">Learning Rate:</label>
          <input type="number" v-model="modelConfig.learningRate" id="learningRate" class="input-field" step="0.005" />
        </div>
  
        <div class="form-group">
          <label for="numEpochs">Number of Epochs:</label>
          <input type="number" v-model="modelConfig.numEpochs" id="numEpochs" class="input-field" />
        </div>
  
        <div class="form-group">
          <label for="batchSize">Batch Size:</label>
          <input type="number" v-model="modelConfig.batchSize" id="batchSize" class="input-field" />
        </div>
  
        <div class="form-group">
          <label for="momentumValue">Momentum Value:</label>
          <input type="number" v-model="modelConfig.momentumValue" id="momentumValue" class="input-field" step="0.1" />
        </div>
  
        <div class="form-group">
          <label for="weightDecay">Weight Decay:</label>
          <input type="number" v-model="modelConfig.weightDecay" id="weightDecay" class="input-field" step="0.0001" />
        </div>
  
        <div class="form-group">
          <label for="sceneId">Scene ID:</label>
          <input type="number" v-model="modelConfig.sceneId" id="sceneId" class="input-field" />
        </div>
  
        <div class="form-group">
          <label for="modelSavePath">Model Save Path:</label>
          <input type="text" v-model="modelConfig.modelSavePath" id="modelSavePath" class="input-field" />
        </div>
  
        <div class="button-group">
          <button type="button" @click="createModelConfig" class="button create-btn">Create Config</button>
          <button type="button" @click="startTraining" class="button train-btn">Start Train</button>
        </div>
      </form>
  
      <!-- 显示操作状态 -->
      <div v-if="responseMessage" class="response-message">
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
  justify-content: space-between;
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