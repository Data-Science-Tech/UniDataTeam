<template>
    <div class="button-group">
        <button type="button" @click="SelectServer" class="button create-btn">确定选择服务器配置</button>
    </div>
</template>


<script setup>
import { ref ,onMounted } from 'vue';
import TrainModelApi from '@/Api/TrainModelApi';
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';

// 初始化 Pinia Store
const globalStore = useGlobalStore();
const router = useRouter();


const SelectServer = async () => {
    try {
        console.log("选择服务器成功:");
        router.push('/uikit/start');
    } catch (error) {
        console.error("选择服务器失败:", error);
    }
}

</script>