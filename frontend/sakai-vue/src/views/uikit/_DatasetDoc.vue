<template>
    <div class="card">
        <div class="font-semibold text-xl mb-4">步骤</div>
        <Stepper value="2">
            <StepList>
                <Step value="1" @click="navigateTo('/uikit/server')">服务器选择</Step>
                <Step value="2" @click="navigateTo('/uikit/dataset')">数据集选择</Step>
                <Step value="3" @click="navigateTo('/uikit/algorithm')">算法选择</Step>
                <Step value="4" @click="navigateTo('/uikit/config')">参数配置</Step>
                <Step value="5" @click="navigateTo('/uikit/start')">训练启动</Step>
            </StepList>
        </Stepper>
    </div>

    <div class="font-semibold text-xl mb-4">场景选择</div>
    <!-- 带有分页、搜索和单选功能的 DataTable -->
    <DataTable 
        :value="scenes" 
        :paginator="true" 
        :rows="10" 
        dataKey="sceneId" 
        :loading="loading" 
        v-model:selection="selectedScenes"
        :filters="filters" 
        v-model:filters="filters" 
        filterDisplay="menu" 
        showGridlines
    >
        <template #header>
            <div class="flex justify-between">
                <!-- 搜索框 -->
                <InputText v-model="filters['global'].value" placeholder="按描述搜索" style="width: 200px" />

                <!-- 清除筛选按钮 -->
                <Button type="button" icon="pi pi-filter-slash" label="清除筛选" outlined @click="clearFilters" />
            </div>
        </template>

        <!-- 空数据时显示的消息 -->
        <template #empty>
            没有找到场景。
        </template>

        <!-- 选择列 -->
        <Column selectionMode="multiple" style="width: 3rem" />

        <!-- 场景ID列 -->
        <Column field="sceneId" header="数据集ID" style="min-width: 10rem" />

        <!-- 场景描述列 -->
        <Column field="sceneDescription" header="数据集描述" style="min-width: 20rem" />

    </DataTable>

    <!-- 确认按钮 -->
    <div class="confirm-group">
        <button 
            type="button" 
            @click="SelectDataset" 
            class="button confirm-btn" 
            :disabled="selectedScenes.length === 0"
        >
            确定数据集选择
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';
// 导入接口
import TrainModelApi from '@/Api/TrainModelApi';

const globalStore = useGlobalStore();
const router = useRouter();

// 本地状态
// 保存初始展示的所有场景
const scenes = ref([]); 
// 保存选中场景的所有信息
const selectedScenes = ref([]); 
const filters = ref({
    global: { value: null },
    name: { value: null },
  });
const loading = ref(false);

// 获取场景数据
const getallscene = async () => {
    try {
        loading.value = true;
        const response = await TrainModelApi.getallscene();
        scenes.value = response.data;
        console.log('场景数据获取成功:', scenes.value);
    } catch (error) {
        console.error('获取场景数据失败:', error);
    } finally {
        loading.value = false;
    }
};

// 清除筛选条件
const clearFilters = () => {
    filters.value = {};
};

// 确定数据集的选择
const SelectDataset = async () => {
    if (selectedScenes.length === 0) {
        alert('请选择至少一个场景');
        return;
    }
    console.log('selectedScenes:', selectedScenes.value);
    globalStore.modelConfig.sceneIds = selectedScenes.value.map(scene => scene.sceneId);
    console.log('选择的场景:', globalStore.modelConfig.sceneIds);
    router.push('/uikit/algorithm');
};

const navigateTo = (path) => {
    router.push(path);
};

// 获取场景数据
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
    color: #fff;
    border: none;
}

.button.primary:hover {
    background-color: #66b1ff;
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
