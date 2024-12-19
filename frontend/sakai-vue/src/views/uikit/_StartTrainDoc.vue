<template>
  <div class="card">
        <div class="font-semibold text-xl mb-4">步骤</div>
        <Stepper value="5">
            <StepList>
                <Step value="1" @click="navigateTo('/uikit/server')">服务器选择</Step>
                <Step value="2" @click="navigateTo('/uikit/dataset')">数据集选择</Step>
                <Step value="3" @click="navigateTo('/uikit/algorithm')">算法选择</Step>
                <Step value="4" @click="navigateTo('/uikit/config')">参数配置</Step>
                <Step value="5" @click="navigateTo('/uikit/start')">训练启动</Step>
            </StepList>
        </Stepper>
    </div>
    <div class="container">
    <h1>模型配置</h1>
    <div class="model-config">
      <ul>
        <li v-for="(value, key) in filteredModelConfig" :key="key">
          <strong>{{ key }}:</strong> {{ value }}
        </li>
      </ul>
    </div>
    <div class="input-group">
      <label for="taskName">任务名称:</label>
      <input type="text" id="taskName" v-model="taskName" />
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

<script setup>
import { ref, computed } from 'vue';
import TrainModelApi from '@/Api/TrainModelApi';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';

const globalStore = useGlobalStore();
const router = useRouter();

const responseMessage = ref('');
const taskName = ref('');

// 过滤掉不需要显示的键
const filteredModelConfig = computed(() => {
  const { status, trainingResults, ...filteredConfig } = globalStore.modelConfig;
  return filteredConfig;
});

// 开始训练模型
const startTraining = async () => {
    try {
        const serverId = globalStore.getServerId();
        const response = await TrainModelApi.startTraining(globalStore.getConfigId(), serverId, taskName.value);
        responseMessage.value = '模型开始训练成功!';
        console.log("模型开始训练成功:", response.data);
        globalStore.setResultId(response.data.id);
    } catch (error) {
        responseMessage.value = '模型训练失败.';
        console.error("模型训练失败:", error);
    }
};

const navigateTo = (path) => {
  router.push(path);
};

</script>



<style scoped>
.container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  color: #000; /* 全局设置文字颜色为黑色 */
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  color: #000; /* 确保 h1 的文字颜色为黑色 */
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
  color: #000; /* 确保列表项的文字颜色为黑色 */
  display: flex;
  align-items: center;
}

strong {
  min-width: 150px; /* 设置一个固定的宽度，保证对齐 */
  margin-right: 10px; /* 给 strong 添加右边距，使值与 key 有间隔 */
  color: #000;
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

.input-group {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}

.input-group label {
  margin-bottom: 5px;
  color: #000; /* 设置输入框标签文字为黑色 */
}

.input-group input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
</style>

