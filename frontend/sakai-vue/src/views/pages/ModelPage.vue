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
              <input
                type="text"
                placeholder="Search Tasks"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
              />
            </div>
            <div class="categories space-y-4">
              <p class="font-semibold text-gray-600">Multimodal</p>
              <button class="category-button">Audio-Text-to-Text</button>
              <button class="category-button">Image-Text-to-Text</button>
              <button class="category-button">Video-Text-to-Text</button>
              <hr />
              <p class="font-semibold text-gray-600">Computer Vision</p>
              <button class="category-button">Depth Estimation</button>
              <button class="category-button">Image Classification</button>
              <button class="category-button">Object Detection</button>
              <hr />
              <p class="font-semibold text-gray-600">Natural Language Processing</p>
              <button class="category-button">Text Classification</button>
              <button class="category-button">Token Classification</button>
              <hr />
              <p class="font-semibold text-gray-600">Machine Learning</p>
              <button class="category-button">Supervised Learning</button>
              <button class="category-button">Unsupervised Learning</button>
              <button class="category-button">Reinforcement Learning</button>
              <hr />
              <p class="font-semibold text-gray-600">Data Science</p>
              <button class="category-button">Data Cleaning</button>
              <button class="category-button">Data Visualization</button>
              <button class="category-button">Big Data</button>
            </div>
          </div>
  
          <!-- 右侧模型展示区域 -->
          <div class="content-section flex-1 bg-gray-50">
            <div class="search-bar mb-6">
              <input
                type="text"
                placeholder="Search Models"
                class="w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
              />
            </div>
            <ul class="models list-none grid grid-cols-2 gap-6 w-full">
              <li v-for="model in models" :key="model.id" class="model-card p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div class="model-header flex items-center mb-2">
                  <img :src="model.icon" alt="模型图标" class="w-8 h-8 mr-2" />
                  <span class="font-semibold">{{ model.name }}</span>
                </div>
                <div class="model-info text-sm text-gray-600">
                  更新时间: {{ model.updateTime }}<br />
                  下载量: {{ model.downloads }}<br />
                  收藏量: {{ model.favorites }}
                </div>
              </li>
              <!-- 添加更多模型样例 -->
              <li v-for="model in additionalModels" :key="model.id" class="model-card p-4 bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div class="model-header flex items-center mb-2">
                  <img :src="model.icon" alt="模型图标" class="w-8 h-8 mr-2" />
                  <span class="font-semibold">{{ model.name }}</span>
                </div>
                <div class="model-info text-sm text-gray-600">
                  更新时间: {{ model.updateTime }}<br />
                  下载量: {{ model.downloads }}<br />
                  收藏量: {{ model.favorites }}
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

  const models = ref([
    {
      id: 1,
      name: "模型名称 A",
      icon: "/src/assets/cool.svg",
      updateTime: "2023-10-01",
      downloads: 1500,
      favorites: 300
    },
    {
      id: 2,
      name: "模型名称 B",
      icon: "/src/assets/cool.svg",
      updateTime: "2023-09-20",
      downloads: 1200,
      favorites: 250
    },
    // ...更多模型
  ]);

  const additionalModels = ref([
    {
      id: 3,
      name: "模型名称 C",
      icon: "/src/assets/cool.svg",
      updateTime: "2023-08-15",
      downloads: 900,
      favorites: 200
    },
    {
      id: 4,
      name: "模型名称 D",
      icon: "/src/assets/cool.svg",
      updateTime: "2023-07-30",
      downloads: 800,
      favorites: 180
    },
    {
      id: 5,
      name: "模型名称 E",
      icon: "/src/assets/cool.svg",
      updateTime: "2023-06-25",
      downloads: 750,
      favorites: 170
    },
    // ...更多模型
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
    margin-top:12px;
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
    transition: all 0.2s ease-in-out, background-color 0.3s, transform 0.3s;
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
  
  .model-card {
    transition: transform 0.2s ease-in-out, transform 0.3s, box-shadow 0.3s;
  }
  
  .model-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
    transform: translateY(-10px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  }
  
  input[type="text"] {
    background-color: #ffffff;
    font-size: 14px;
    transition: box-shadow 0.3s;
  }

  input[type="text"]:focus {
    box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
  }

  .models {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    width: 100%;
    margin: 0 auto;
  }

  .model-card {
    list-style: none;
    width: 100%;
  }

  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  </style>
