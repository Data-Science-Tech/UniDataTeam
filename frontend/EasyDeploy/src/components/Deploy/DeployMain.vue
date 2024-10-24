<template>
        <HeaderComponent />
        <div class="content">
                <Sidebar />
                <div class="main-content">
                        <ConfigurationSelection />
                        <NodeSelection />
                        <VirtualEnv />
                        <Log />
                        <PerformanceParameters />
                        <Service />
                        <Acceleration />
                </div>
        </div>
</template>

<script setup>
import HeaderComponent from '@/components/Home/HeaderComponent.vue';
import Sidebar from '@/components/Deploy/Sidebar.vue';
import ConfigurationSelection from '@/components/Deploy/ConfigurationSelection.vue';
import NodeSelection from '@/components/Deploy/NodeSelection.vue';
import VirtualEnv from '@/components/Deploy/VirtualEvn.vue';
import Log from '@/components/Deploy/Log.vue';
import PerformanceParameters from '@/components/Deploy/PerformanceParameters.vue';
import Service from '@/components/Deploy/Service.vue';
import Acceleration from '@/components/Deploy/Acceleration.vue'



</script>

<style scoped>
.sidebar {
        width: 150px;
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