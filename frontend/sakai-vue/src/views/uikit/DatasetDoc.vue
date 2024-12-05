<template>
    <div class="card">
        <div class="font-semibold text-xl mb-4">步骤</div>
        <Stepper value="2">
            <StepList>
                <Step value="1">服务器选择</Step>
                <Step value="2">数据集选择</Step>
                <Step value="3">算法选择</Step>
                <Step value="4">参数配置</Step>
                <Step value="5">训练启动</Step>
            </StepList>
        </Stepper>
    </div>

    <label for="scene">场景ID:</label>
    <MultiSelect v-model="globalStore.modelConfig.sceneIds" :options="scenes" optionLabel="sceneDescription"
        optionValue="sceneId" placeholder="请选择场景" :filter="true">
        <template #value="slotProps">
            <div class="inline-flex items-center py-1 px-2 bg-primary text-primary-contrast rounded-border mr-2"
                v-for="option of slotProps.value" :key="option">
                <div>{{ getSceneDescriptionById(option) }}</div>
            </div>
            <template v-if="!slotProps.value || slotProps.value.length === 0">
                <div class="p-1">请选择场景</div>
            </template>
        </template>
        <template #option="slotProps">
            <div class="flex items-center">
                <div>{{ slotProps.option.sceneId }} - {{ slotProps.option.sceneDescription }}</div>
            </div>
        </template>
    </MultiSelect>

    <!-- 确认按钮 -->
    <button type="button" @click="SelectDataset" class="button confirm-btn">
        确定数据集选择
    </button>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';
// 导入接口
import TrainModelApi from '@/Api/TrainModelApi';

// 初始化 Pinia Store 和 Router
const globalStore = useGlobalStore();
const router = useRouter();
// 本地状态
const scenes = ref([]); // 场景数据

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


const getSceneDescriptionById = (sceneId) => {
    const scene = scenes.value.find(item => item.sceneId === sceneId);
    return scene ? scene.sceneDescription : '';
};


// 确定数据集的选择
const SelectDataset = async () => {
    console.log('选择的数据集:',globalStore.modelConfig.sceneIds);
    router.push('/uikit/algorithm');
};


// 组件挂载时获取场景数据
onMounted(getallscene);
</script>

<style scoped>
.button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.button {
    font-size: 1rem;
    padding: 10px 15px;
    border-radius: 5px;
    border: 1px solid #ddd;
    background-color: #fff;
    color: #333;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    background-color: #f0f0f0;
    border-color: #ccc;
}

.button.primary {
    background-color: #409eff;
    /* 主色调 */
    color: #fff;
    border: none;
}

.button.primary:hover {
    background-color: #66b1ff;
    /* 悬停色 */
}

.button:disabled {
    background-color: #ccc;
    color: #999;
    cursor: not-allowed;
}

.confirm-group {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.confirm-btn {
    background-color: #2d8cf0;
    color: white;
    font-size: 16px;
}
</style>