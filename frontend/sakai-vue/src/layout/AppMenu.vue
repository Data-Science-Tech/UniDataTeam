<script setup>
import { ref } from 'vue';
import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: '主页',
        items: [{ label: '首页', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    // {
    //     label: '工作台',
    //     items: [{ label: '工作台', icon: 'pi pi-fw pi-desktop', to: '/workbench' }]
    // },
    {
        label: '数据与算法管理',
        items: [
            { label: '非统一数据集导入', icon: 'pi pi-fw pi-upload', to: '/uikit/formlayout' },
            { label: '数据集格式转换', icon: 'pi pi-fw pi-sync', to: '/uikit/input' },
            { label: '算法导入', icon: 'pi pi-fw pi-list', to: '/uikit/button' },
            { label: '算法适配', icon: 'pi pi-fw pi-cog', to: '/uikit/table' }
        ]
    },
    {
        label: '训练管理',
        items: [
            { label: '服务器选择', icon: 'pi pi-fw pi-server', to: '/uikit/server' },
            { label: '数据集选择', icon: 'pi pi-fw pi-server', to: '/uikit/dataset' },
            { label: '算法选择', icon: 'pi pi-fw pi-server', to: '/uikit/algorithm' },
            { label: '参数配置', icon: 'pi pi-fw pi-sliders-h', to: '/uikit/config' },
            { label: '训练启动', icon: 'pi pi-fw pi-play', to: '/uikit/start' },
        
        ]
    },
    {
        label: '任务管理',
        items: [
            { label: '任务概览', icon: 'pi pi-fw pi-info-circle', to: '/uikit/overlay' },
        ]
    },
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
