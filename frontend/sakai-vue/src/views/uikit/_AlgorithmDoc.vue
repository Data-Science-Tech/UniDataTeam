<template>
    <div class="card">
      <div class="font-semibold text-xl mb-4">步骤</div>
      <Stepper value="3">
        <StepList>
          <Step value="1" @click="navigateTo('/uikit/server')">服务器选择</Step>
          <Step value="2" @click="navigateTo('/uikit/dataset')">数据集选择</Step>
          <Step value="3" @click="navigateTo('/uikit/algorithm')">算法选择</Step>
          <Step value="4" @click="navigateTo('/uikit/config')">参数配置</Step>
          <Step value="5" @click="navigateTo('/uikit/start')">训练启动</Step>
        </StepList>
      </Stepper>
    </div>
    <div class="card">
      <div class="font-semibold text-xl mb-4">算法列表</div>
  
      <!-- 带有分页、搜索和单选功能的DataTable -->
      <DataTable :value="algorithms" :paginator="true" :rows="10" dataKey="id" :rowHover="true" :loading="loading"
        :filters="filters" v-model:filters="filters" filterDisplay="menu" showGridlines
        v-model:selection="selectedAlgorithm">
        <template #header>
          <div class="flex justify-between">
            <!-- 搜索框 -->
            <InputText v-model="filters['global'].value" placeholder="按名称搜索" style="width: 200px" />
  
            <!-- 清除筛选按钮 -->
            <Button type="button" icon="pi pi-filter-slash" label="清除筛选" outlined @click="clearFilters" />
          </div>
        </template>
  
        <!-- 空数据时显示的消息 -->
        <template #empty>
          没有找到算法。
        </template>
  
        <!-- 选择列 -->
        <Column selectionMode="single" style="width: 3rem" />
  
        <!-- 列 -->
        <Column field="name" header="算法名称" style="min-width: 14rem" />
  
        <Column header="类别" filterField="category" style="min-width: 12rem">
          <template #body="{ data }">
            <span>{{ data.category }}</span>
          </template>
          <template #filter="{ filterModel }">
            <MultiSelect v-model="filterModel.value" :options="categories" optionLabel="name" placeholder="选择类别" :showClear="true" />
          </template>
        </Column>
  
        <Column header="日期" filterField="date" dataType="date" style="min-width: 10rem">
          <template #body="{ data }">
            {{ formatDate(data.date) }}
          </template>
          <template #filter="{ filterModel }">
            <InputText v-model="filterModel.value" type="date" />
          </template>
        </Column>
      </DataTable>
    </div>
  
    <!-- 确认按钮 -->
    <button type="button" @click="SelectAlgorithms" class="button confirm-btn">
      确定算法选择
    </button>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useGlobalStore } from '@/stores/ConfigStore.js';
  import { useRouter } from 'vue-router';
  
  // 初始化 Pinia Store 和 Router
  const globalStore = useGlobalStore();
  const router = useRouter();
  
  // 组件状态
  const loading = ref(false);
  const filters = ref({
    global: { value: null },
    name: { value: null },
    category: { value: null },
    date: { value: null },
  });
  
  // 算法列表，使用英文数据
  const algorithms = ref([
    { id: 1, name: 'FAST_R_CNN', category: 'Perception', date: '2024-01-01' },
    { id: 2, name: 'SSD', category: 'Perception', date: '2024-02-01' },
  ]);
  
  // 保存选中的算法（只包含id和name）
  const selectedAlgorithm = ref([]);
  
  // 清除所有筛选器
  const clearFilters = () => {
    filters.value = {
      global: { value: null },
      name: { value: null },
      category: { value: null },
      date: { value: null },
    };
  };
  
  // 格式化日期
  const formatDate = (date) => {
    const d = new Date(date);
    return `${d.getFullYear()}/${d.getDate()}/${d.getMonth() + 1}`;
  };
  
  // 处理算法选择
  const SelectAlgorithms = async () => {
    globalStore.modelConfig.algorithm = selectedAlgorithm.value.name;
    console.log('selectedAlgorithm:', selectedAlgorithm.value);
    console.log('selectedAlgorithm.name:', selectedAlgorithm.value.name);
    console.log('选择的算法:', globalStore.modelConfig.algorithm);
    router.push('/uikit/config');
  };

  const navigateTo = (path) => {
    router.push(path);
  };
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
