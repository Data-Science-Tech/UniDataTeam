<template>
    <div class="card">
        <h1 class="text-3xl font-bold mb-4">任务管理</h1>

        <!-- Search Bar -->
        <div class="flex justify-between mb-4">
            <div class="flex gap-2">
                <Button label="新建任务" icon="pi pi-plus" severity="success" @click="goToNewTaskPage"  />
                <!-- <Button label="批量管理" icon="pi pi-cog" severity="secondary" /> -->
            </div>
            <!-- 右侧搜索框 -->
            <div class="flex gap-2 items-center">
                <i class="pi pi-search mr-2"></i> <!-- 图标和输入框之间有个小间距 -->
                <InputText v-model="filters['global'].value" placeholder="搜索任务..." class="w-full" />
            </div>
        </div>

        <!-- Data Table -->
        <!-- globalFilterFields指定被搜索的值
        'userServerName', 'status', 'serverTypeName', 'gpuType' -->
        <DataTable :value="missions" :paginator="true" :rows="10" :filters="filters" dataKey="id" filterDisplay="menu"
            :globalFilterFields="['userServerName', 'status', 'serverTypeName', 'gpuType']"
            tableStyle="min-width: 80rem"
            selectionMode="single"
            @rowSelect="onRowSelect">
            <!-- Task Name -->
            <Column field="userServerName" header="训练任务名称" sortable style="min-width: 12rem"></Column>

            <!-- Status -->
            <Column field="status" header="训练状态" sortable style="min-width: 8rem">
                <template #body="slotProps">
                    <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
                </template>
            </Column>

            <!-- Server Name -->
            <Column field="serverTypeName" header="服务器名称" sortable style="min-width: 12rem"></Column>

            <!-- Price per Hour -->
            <Column field="pricePerHour" header="服务器价格" sortable style="min-width: 10rem"></Column>

            <!-- Description -->
            <Column field="description" header="服务器描述" style="min-width: 14rem"></Column>

            <!-- GPU Type -->
            <Column field="gpuType" header="GPU类型" style="min-width: 10rem"></Column>

            <!-- RAM Size -->
            <Column field="ramSize" header="内存大小 (GB)" style="min-width: 10rem"></Column>

            <!-- vCPU Number -->
            <Column field="vcpuNum" header="vCPU 数量" style="min-width: 8rem"></Column>

            <!-- Start Time -->
            <Column field="startTime" header="开始时间" style="min-width: 12rem">
                <template #body="slotProps">
                    {{ formatDate(slotProps.data.startTime) }}
                </template>
            </Column>

            <!-- End Time -->
            <Column field="endTime" header="结束时间" style="min-width: 12rem">
                <template #body="slotProps">
                    {{ formatDate(slotProps.data.endTime) }}
                </template>
            </Column>

            <!-- Training Logs -->
            <Column field="trainingLogs" header="训练日志路径" style="min-width: 12rem"></Column>

            <!-- Model File Path -->
            <Column field="modelFilePath" header="训练模型路径" style="min-width: 12rem"></Column>

        </DataTable>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useGlobalStore } from '@/stores/ConfigStore.js';
// 导入接口
import GetAllTasksApi from '@/Api/GetAllTasksApi.js';

const router = useRouter();
const globalStore = useGlobalStore();
const missions = ref([]);
const filters = ref({
    global: { value: null, matchMode: 'contains' }
});

// 获取任务数据
const getalltest = async () => {
    try {
        // 传入登录用户的id
        const globalStore = useGlobalStore();
        const userId = globalStore.userId;
        const response = await GetAllTasksApi.getalltests(userId);
        missions.value = response.data;
        console.log('任务数据获取成功:', missions.value);
    } catch (error) {
        console.error('任务场景数据失败:', error);
    }
};

const getStatusSeverity = (status) => {
    switch (status) {
        case 'RUNNING':
            return 'success';
        case 'STOPPED':
            return 'danger';
        default:
            return 'info';
    }
};

const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString();
};

// 跳转到新建任务页面
const goToNewTaskPage = () => {
    console.log('跳转到服务器选择页面');
    globalStore.resetForm();
    router.push('/uikit/server');
};

// 添加行选择处理函数
const onRowSelect = (event) => {
    router.push(`/pages/missionManage/missionDetail/${event.data.id}/${event.data.modelConfigId}`);
};

// 获取任务数据
onMounted(getalltest);
</script>

<style scoped>
.p-input-icon-left {
    width: 100%;
}

.p-input-icon-left input {
    width: 100%;
}
</style>
