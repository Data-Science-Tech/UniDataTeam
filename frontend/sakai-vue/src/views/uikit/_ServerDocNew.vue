<template>
    <div class="card">
        <div class="font-semibold text-xl mb-4">步骤</div>
        <Stepper value="1">
            <StepList>
                <Step value="1" @click="navigateTo('/uikit/server')">服务器选择</Step>
                <Step value="2" @click="navigateTo('/uikit/dataset')">数据集选择</Step>
                <Step value="3" @click="navigateTo('/uikit/algorithm')">算法选择</Step>
                <Step value="4" @click="navigateTo('/uikit/config')">参数配置</Step>
                <Step value="5" @click="navigateTo('/uikit/start')">训练启动</Step>
            </StepList>
        </Stepper>
    </div>

    <div class="font-semibold text-xl mb-4">服务器选择</div>
    <!-- 带有分页、搜索和单选功能的 DataTable -->
    <DataTable 
        :value="servers" 
        :paginator="true" 
        :rows="10" 
        dataKey="id" 
        :loading="loading" 
        v-model:selection="selectedServer"
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
            没有找到服务器。
        </template>

        <!-- 选择列 -->
        <Column selectionMode="single" style="width: 3rem" />

        <!-- 服务器名称列 -->
        <Column field="name" header="服务器名称" style="min-width: 10rem" />

        <!-- 服务器描述列 -->
        <Column field="description" header="服务器描述" style="min-width: 20rem" />

        <!-- GPU类型列 -->
        <Column field="gpuType" header="GPU类型" style="min-width: 10rem" />

        <!-- 内存大小列 -->
        <Column field="ramSize" header="内存大小(GB)" style="min-width: 10rem" />

        <!-- vCPU数量列 -->
        <Column field="vcpuNum" header="vCPU数量" style="min-width: 10rem" />

        <!-- 每小时价格列 -->
        <Column field="pricePerHour" header="每小时价格($)" style="min-width: 10rem" />
    </DataTable>

    <!-- 确认按钮 -->
    <div class="confirm-group">
        <button 
            type="button" 
            @click="SelectServer" 
            class="button confirm-btn" 
            :disabled="!selectedServer"
        >
            确定服务器选择
        </button>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';
import GetAllServers from '@/Api/GetAllServers';

const globalStore = useGlobalStore();
const router = useRouter();

// 本地状态
const servers = ref([]); 
const selectedServer = ref(null); // 确保 selectedServer 是一个对象
const filters = ref({
    global: { value: null },
    name: { value: null },
});
const loading = ref(false);

// 获取服务器数据
const getAllServers = async () => {
    try {
        loading.value = true;
        const response = await GetAllServers();
        servers.value = response.data;
        console.log('服务器数据获取成功:', servers.value);
    } catch (error) {
        console.error('获取服务器数据失败:', error);
    } finally {
        loading.value = false;
    }
};

// 清除筛选条件
const clearFilters = () => {
    filters.value = {};
};

// 确定服务器的选择
const SelectServer = async () => {
    if (!selectedServer.value) {
        alert('请选择一个服务器');
        return;
    }
    console.log('selectedServer:', selectedServer.value);
    globalStore.serverId = selectedServer.value.id;
    console.log('选择的服务器:', globalStore.serverId);
    router.push('/uikit/dataset');
};

const navigateTo = (path) => {
    router.push(path);
};

// 获取服务器数据
onMounted(getAllServers);
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
