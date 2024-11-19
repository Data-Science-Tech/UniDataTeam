<script setup>
import { ref } from 'vue';
import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: '主页',
        items: [{ label: '首页', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: '工作台',
        items: [{ label: '工作台', icon: 'pi pi-fw pi-desktop', to: '/workbench' }]
    },
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
            { label: '一键训练启动', icon: 'pi pi-fw pi-play', to: '/uikit/list' },
            { label: '训练参数配置', icon: 'pi pi-fw pi-sliders-h', to: '/uikit/tree' },
            { label: '服务器端训练执行', icon: 'pi pi-fw pi-server', to: '/uikit/panel' }
        ]
    },
    {
        label: '训练监控',
        items: [
            { label: '训练状态反馈', icon: 'pi pi-fw pi-info-circle', to: '/uikit/overlay' },
            { label: '训练进度展示', icon: 'pi pi-fw pi-chart-line', to: '/uikit/media' }
        ]
    },
    {
        label: '训练结果管理',
        items: [
            { label: '模型文件生成', icon: 'pi pi-fw pi-file', to: '/uikit/menu' },
            { label: '训练数据与日志存储', icon: 'pi pi-fw pi-database', to: '/uikit/message' },
            { label: '结果文件下载', icon: 'pi pi-fw pi-download', to: '/uikit/file' },
            { label: '操作日志记录', icon: 'pi pi-fw pi-book', to: '/uikit/charts' },
            { label: '历史记录追踪', icon: 'pi pi-fw pi-history', to: '/uikit/timeline' }
        ]
    }
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
