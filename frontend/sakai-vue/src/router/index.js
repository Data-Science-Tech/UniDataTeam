import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('@/views/pages/Home.vue')
        },
        {
            path: '/workbench',
            component: AppLayout,
            children: [
                {
                    path: '',
                    name: 'train',
                    component: () => import('@/views/pages/TrainConfig/SaveConfig.vue')
                },
                {
                    path: '/uikit/formlayout',
                    name: 'formlayout',
                    component: () => import('@/views/uikit/FormLayout.vue')
                },
                {
                    path: '/uikit/input',
                    name: 'input',
                    component: () => import('@/views/uikit/InputDoc.vue')
                },
                {
                    path: '/uikit/button',
                    name: 'button',
                    component: () => import('@/views/uikit/ButtonDoc.vue')
                },
                {
                    path: '/uikit/table',
                    name: 'table',
                    component: () => import('@/views/uikit/TableDoc.vue')
                },
                // 自定义路由
                // 服务器选择
                {
                    path: '/uikit/server',
                    name: 'Server',
                    component: () => import('@/views/uikit/ServerDoc.vue')
                },
                // 数据集选择
                {
                    path: '/uikit/dataset',
                    name: 'Dataset',
                    component: () => import('@/views/uikit/DatasetDoc.vue')
                },
                // 算法选择
                {
                    path: '/uikit/algorithm',
                    name: 'Algorithm',
                    component: () => import('@/views/uikit/AlgorithmDoc.vue')
                },
                //配置选择
                {
                    path: '/uikit/config',
                    name: 'Config',
                    component: () => import('@/views/uikit/ConfigDoc.vue')
                },
                //开始训练选择
                {
                    path: '/uikit/start',
                    name: 'Start',
                    component: () => import('@/views/uikit/StartTrainDoc.vue')
                },
                // 自定义路由结束
                {
                    path: '/uikit/panel',
                    name: 'panel',
                    component: () => import('@/views/uikit/PanelsDoc.vue')
                },

                {
                    path: '/uikit/overlay',
                    name: 'overlay',
                    component: () => import('@/views/uikit/OverlayDoc.vue')
                },
                {
                    path: '/uikit/media',
                    name: 'media',
                    component: () => import('@/views/uikit/MediaDoc.vue')
                },
                {
                    path: '/uikit/message',
                    name: 'message',
                    component: () => import('@/views/uikit/MessagesDoc.vue')
                },
                {
                    path: '/uikit/file',
                    name: 'file',
                    component: () => import('@/views/uikit/FileDoc.vue')
                },
                {
                    path: '/uikit/menu',
                    name: 'menu',
                    component: () => import('@/views/uikit/MenuDoc.vue')
                },
                {
                    path: '/uikit/charts',
                    name: 'charts',
                    component: () => import('@/views/uikit/ChartDoc.vue')
                },
                {
                    path: '/uikit/misc',
                    name: 'misc',
                    component: () => import('@/views/uikit/MiscDoc.vue')
                },
                {
                    path: '/uikit/timeline',
                    name: 'timeline',
                    component: () => import('@/views/uikit/TimelineDoc.vue')
                },
                {
                    path: '/pages/empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: '/pages/crud',
                    name: 'crud',
                    component: () => import('@/views/pages/Crud.vue')
                },
                {
                    path: '/documentation',
                    name: 'documentation',
                    component: () => import('@/views/pages/Documentation.vue')
                }
            ]
        },
        {
            path: '/pages/notfound',
            name: 'notfound',
            component: () => import('@/views/pages/NotFound.vue')
        },
        {
            path: '/model',
            name: 'model',
            component: () => import('@/views/pages/ModelPage.vue')
        },
        {
            path: '/dataset',
            name: 'dataset',
            component: () => import('@/views/pages/DatasetPage.vue')
        },
        {
            path: '/auth/login',
            name: 'login',
            component: () => import('@/views/pages/auth/Login.vue')
        },
        {
            path: '/auth/access',
            name: 'accessDenied',
            component: () => import('@/views/pages/auth/Access.vue')
        },
        {
            path: '/auth/error',
            name: 'error',
            component: () => import('@/views/pages/auth/Error.vue')
        },
    ]
});

export default router;
