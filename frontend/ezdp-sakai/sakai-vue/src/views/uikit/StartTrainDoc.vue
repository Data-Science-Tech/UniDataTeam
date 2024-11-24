<script setup>
import { ref ,computed } from 'vue';
import TrainModelApi from '@/Api/TrainModelApi';
import { useGlobalStore } from '@/stores/ConfigStore.js';
// 获取 Pinia store 的实例
const globalStore = useGlobalStore();


const responseMessage = ref('');

// 过滤掉不需要显示的键
const filteredModelConfig = computed(() => {
  const { status, trainingResults, ...filteredConfig } = globalStore.modelConfig;
  return filteredConfig;
});


// 开始训练模型
const startTraining = async () => {
    try {
        console.log(globalStore.getConfigId());
        const response = await TrainModelApi.startTraining(globalStore.getConfigId());
        responseMessage.value = '模型开始训练成功!';
        console.log("模型开始训练成功:", response.data);
        globalStore.setResultId(response.data.id);
    } catch (error) {
        responseMessage.value = '模型训练失败.';
        console.error("模型训练失败:", error);
    }
};

</script>

<template>
    <div class="container">
    <h1>模型配置</h1>
    <div class="model-config">
      <ul>
        <li v-for="(value, key) in filteredModelConfig" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </div>
  </div>
  <!-- 显示操作状态 -->
  <div v-if="responseMessage" class="response-message">
            <p>{{ responseMessage }}</p>
        </div>
    <div class="button-group">
        <button type="button" @click="startTraining" class="button create-btn">开始训练</button>
    </div>
</template>


<style scoped>
.container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.model-config {
  margin-top: 20px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin: 10px 0;
  padding: 8px;
  background-color: #f4f4f4;
  border-radius: 4px;
}

strong {
  color: #007bff;
}
.button {
  padding: 10px 15px;
  color: #fff;
  background-color: #007bff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.button-group {
    display: flex;
    justify-content: center; 
    align-items: center; 
}
.button:hover {
  background-color: #0056b3;
}
</style>