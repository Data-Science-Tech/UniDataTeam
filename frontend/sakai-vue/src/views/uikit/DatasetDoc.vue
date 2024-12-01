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

    <!-- 确认按钮 -->
    <button type="button" @click="SelectDataset" class="button confirm-btn">
        确定数据集选择
    </button>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';

// 初始化 Pinia Store 和 Router
const globalStore = useGlobalStore();
const router = useRouter();


// 处理数据集选择
const SelectDataset = async () => {
    console.log('选择的数据集:', );
    router.push('/uikit/algorithm');
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