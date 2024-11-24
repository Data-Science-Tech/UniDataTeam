<template>
    <div class="full-height">
        <div class="header">
            <HeaderComponent />
        </div>
        <div class="container mx-auto px-6 py-4">
            <div class="main-content flex gap-6">
                <!-- 左侧过滤区域 -->
                <div class="filter-section w-1/4 bg-white rounded-lg shadow p-4 flex flex-col justify-between">
                    <div class="search-box mb-6">
                        <input type="text" placeholder="搜索数据集" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300" />
                    </div>
                    <div class="categories space-y-4">
                        <p class="font-semibold text-gray-600">类别</p>
                        <button class="category-button">图像数据集</button>
                        <button class="category-button">文本数据集</button>
                        <button class="category-button">音频数据集</button>
                        <hr />
                        <p class="font-semibold text-gray-600">用途</p>
                        <button class="category-button">分类</button>
                        <button class="category-button">回归</button>
                        <button class="category-button">聚类</button>
                        <!-- ...更多分类 -->
                    </div>
                </div>

                <!-- 右侧数据集展示区域 -->
                <div class="content-section flex-1 bg-gray-50">
                    <div class="search-bar mb-6">
                        <input type="text" placeholder="搜索数据集" class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300" />
                    </div>
                    <ul class="datasets list-none grid grid-cols-2 gap-6 w-full">
                        <li v-for="dataset in datasets" :key="dataset.id" class="dataset-card p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                            <div class="dataset-header flex items-center mb-2">
                                <img :src="dataset.icon" alt="数据集图标" class="w-8 h-8 mr-2" />
                                <span class="font-semibold">{{ dataset.name }}</span>
                            </div>
                            <div class="dataset-info text-sm text-gray-600">
                                更新日期: {{ dataset.updateTime }}<br />
                                下载量: {{ dataset.downloads }}<br />
                                收藏量: {{ dataset.favorites }}
                            </div>
                        </li>
                        <!-- 添加更多数据集样例 -->
                        <li v-for="dataset in additionalDatasets" :key="dataset.id" class="dataset-card p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                            <div class="dataset-header flex items-center mb-2">
                                <img :src="dataset.icon" alt="数据集图标" class="w-8 h-8 mr-2" />
                                <span class="font-semibold">{{ dataset.name }}</span>
                            </div>
                            <div class="dataset-info text-sm text-gray-600">
                                更新日期: {{ dataset.updateTime }}<br />
                                下载量: {{ dataset.downloads }}<br />
                                收藏量: {{ dataset.favorites }}
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import HeaderComponent from '@/components/Home/HeaderComponent.vue';
import { ref } from 'vue';

const datasets = ref([
    {
        id: 1,
        name: '数据集名称 A',
        icon: '/src/assets/dataset.svg',
        updateTime: '2023-10-01',
        downloads: 1500,
        favorites: 300
    },
    {
        id: 2,
        name: '数据集名称 B',
        icon: '/src/assets/dataset.svg',
        updateTime: '2023-09-20',
        downloads: 1200,
        favorites: 250
    }
    // ...更多数据集
]);

const additionalDatasets = ref([
    {
        id: 3,
        name: '数据集名称 C',
        icon: '/src/assets/dataset.svg',
        updateTime: '2023-08-15',
        downloads: 900,
        favorites: 200
    },
    {
        id: 4,
        name: '数据集名称 D',
        icon: '/src/assets/dataset.svg',
        updateTime: '2023-07-30',
        downloads: 800,
        favorites: 180
    },
    {
        id: 5,
        name: '数据集名称 E',
        icon: '/src/assets/dataset.svg',
        updateTime: '2023-06-25',
        downloads: 750,
        favorites: 170
    }
    // ...更多数据集
]);
</script>

<style scoped>
.full-height {
    /*height: 100vh !important;*/
    display: flex;
    flex-direction: column;
    background-color: #f7f8fa;
    /* animation: fadeIn 1s ease-in-out; */
    transition: all 0.3s ease-in-out;
}

.header {
    margin-top: 12px;
}

.container {
    max-width: 1500px !important;
    margin: 0 auto !important;
}

.filter-section {
    /*background-color: #ffffff;*/
    border-radius: 8px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease-in-out;
}

.filter-section:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.category-button {
    display: block;
    width: 100%;
    text-align: left;
    padding: 8px 12px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    background-color: #ffffff;
    font-size: 14px;
    color: #333;
    cursor: pointer;
    transition:
        all 0.2s ease-in-out,
        background-color 0.3s,
        transform 0.3s;
}

.category-button:hover {
    background-color: #f3f4f6;
    border-color: #cbd5e1;
    background-color: #e0e0e0;
    transform: translateX(5px);
}

.content-section {
    flex-grow: 1;
}

.dataset-card {
    transition:
        transform 0.2s ease-in-out,
        transform 0.3s,
        box-shadow 0.3s;
}

.dataset-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    transform: translateY(-10px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

input[type='text'] {
    background-color: #ffffff;
    font-size: 14px;
    transition: box-shadow 0.3s;
}

input[type='text']:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.datasets {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    width: 100%;
    margin: 0 auto;
}

.dataset-card {
    list-style: none;
    width: 100%;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
</style>
