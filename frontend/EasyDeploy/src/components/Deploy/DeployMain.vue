<template>
        <HeaderComponent />
        <div class="content">
                <Sidebar />
                <div class="main-content">
                        <h2 class="prompt">环境配置</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">节点选择</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">虚拟环境搭建</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">日志与性能检测</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">性能参数</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">服务组件</h2>
                        <ConfigurationSelection />
                        <h2 class="prompt">性能加速</h2>
                        <ConfigurationSelection />
                </div>
        </div>
</template>

<script setup>
import HeaderComponent from '@/components/Home/HeaderComponent.vue';
import ConfigurationSelection from '@/components/Deploy/ConfigurationSelection.vue';
import Sidebar from '@/components/Deploy/Sidebar.vue';


</script>

<style scoped>
.sidebar {
        width: 250px;
        background-color: #d82d2d;
        padding: 20px;
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.content {
        display: flex;
        height: 100vh;
}

.main-content {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
        padding: 20px;
        background-color: #fff;
}

.prompt {
        font-size: 35px;
        color: #212529;
        text-align: center;
}
</style>