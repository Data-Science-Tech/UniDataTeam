<script setup>
import { ref, onBeforeMount } from 'vue';

const missions = ref(null);
const filters = ref({
    global: { value: null, matchMode: 'contains' }
});

onBeforeMount(() => {
    // 模拟数据
    missions.value = [
        {
            id: '1',
            name: 'AI训练任务-01',
            status: '运行中',
            specs: 'GPU: RTX 3080 16GB',
            diskUsage: '120GB/500GB',
            health: '正常',
            paymentMode: '按量付费',
            runningTime: '72小时',
            sshAccess: 'enabled',
        },
        {
            id: '2',
            name: '数据处理任务-02',
            status: '已停止',
            specs: 'CPU: 16核 32GB内存',
            diskUsage: '50GB/200GB',
            health: '警告',
            paymentMode: '包月',
            runningTime: '24小时',
            sshAccess: 'disabled',
        }
    ];
});

const getStatusSeverity = (status) => {
    switch (status) {
        case '运行中':
            return 'success';
        case '已停止':
            return 'danger';
        default:
            return null;
    }
};

const getHealthSeverity = (health) => {
    switch (health) {
        case '正常':
            return 'success';
        case '警告':
            return 'warn';
        default:
            return 'danger';
    }
};
</script>

<template>
    <div class="card">
        <h1 class="text-3xl font-bold mb-4">任务管理</h1>
        
        <div class="flex justify-between mb-4">
            <div class="flex gap-2">
                <Button label="新建任务" icon="pi pi-plus" severity="success" />
                <Button label="批量管理" icon="pi pi-cog" severity="secondary" />
            </div>
            <div class="flex">
                <div class="p-input-icon-left">
                    <i class="pi pi-search" />
                    <InputText v-model="filters['global'].value" placeholder="搜索任务..." />
                </div>
            </div>
        </div>

        <DataTable
            :value="missions"
            :paginator="true"
            :rows="10"
            :filters="filters"
            dataKey="id"
            filterDisplay="menu"
            :globalFilterFields="['name', 'status', 'specs']"
            tableStyle="min-width: 60rem"
        >
            <Column field="name" header="名称" sortable style="min-width: 12rem"></Column>
            <Column field="status" header="状态" sortable style="min-width: 8rem">
                <template #body="slotProps">
                    <Tag :value="slotProps.data.status" :severity="getStatusSeverity(slotProps.data.status)" />
                </template>
            </Column>
            <Column field="specs" header="规格详情" style="min-width: 14rem"></Column>
            <Column field="diskUsage" header="本地磁盘" style="min-width: 10rem"></Column>
            <Column field="health" header="健康状态" style="min-width: 8rem">
                <template #body="slotProps">
                    <Tag :value="slotProps.data.health" :severity="getHealthSeverity(slotProps.data.health)" />
                </template>
            </Column>
            <Column field="paymentMode" header="付费模式" style="min-width: 8rem"></Column>
            <Column field="runningTime" header="运行时间" style="min-width: 8rem"></Column>
            <Column field="sshAccess" header="SSH登录" style="min-width: 8rem">
                <template #body="slotProps">
                    <Tag :value="slotProps.data.sshAccess === 'enabled' ? '已启用' : '未启用'"
                         :severity="slotProps.data.sshAccess === 'enabled' ? 'success' : 'danger'" />
                </template>
            </Column>
            <Column header="操作" style="min-width: 12rem">
                <template #body>
                    <div class="flex gap-2">
                        <Button icon="pi pi-pencil" text severity="info" />
                        <Button icon="pi pi-trash" text severity="danger" />
                        <Button icon="pi pi-stop-circle" text severity="warning" />
                    </div>
                </template>
            </Column>
        </DataTable>
    </div>
</template>

<style scoped>
.p-input-icon-left {
    width: 100%;
}
.p-input-icon-left input {
    width: 100%;
}
</style>
