<template>
    <div class="dashboard">
      <!-- 顶部状态栏 -->
      <div class="status-bar">
        <button v-for="status in statuses" :key="status" :class="['status-btn', status.class]">
          <div class="flex-row justify-between items-center page">
            <div class="flex-col justify-start image-wrapper">
              <img class="image" :src="status.icon" />
            </div>
            <span class="text">{{ status.label }}</span>
          </div>
        </button>
      </div>
  
      <!-- 环境配置 -->
      <section class="env-setup">
        <h2>环境配置</h2>
        <div class="env-container">
          <div class="env-menu">
            <button class="menu-btn active">操作系统</button>
            <button class="menu-btn">架构</button>
            <button class="menu-btn">...</button>
          </div>
          <div class="env-options">
            <div class="os-options">
              <button v-for="os in osOptions" :key="os" :class="['os-btn', { active: selectedOS === os }]" @click="selectOS(os)">
                {{ os }}
              </button>
            </div>
            <div class="arch-options">
              <button v-for="arch in archOptions" :key="arch" :class="['arch-btn', { active: selectedArch === arch }]" @click="selectArch(arch)">
                {{ arch }}
              </button>
            </div>
          </div>
        </div>
      </section>
  
      <!-- 节点选择 -->
      <section class="node-selection">
        <h2>节点选择</h2>
        <div class="cloud-options">
          <button v-for="provider in cloudProviders" :key="provider" :class="['cloud-btn', { active: selectedCloud === provider }]" @click="selectCloud(provider)">
            {{ provider }}
          </button>
        </div>
        <div class="node-options">
          <div v-for="node in nodes" :key="node.id" class="node">
            <span>{{ node.name }}</span>
            <span>{{ node.details }}</span>
          </div>
        </div>
      </section>
  
      <!-- 虚拟环境搭建 -->
      <section class="virtual-env">
        <h2>虚拟环境搭建</h2>
        <input type="file" @change="uploadYaml" />
      </section>
  
      <!-- 日志与性能监测 -->
      <section class="logs-performance">
        <h2>日志与性能监测</h2>
        <div class="log-options">
          <button>日志</button>
          <button>性能监测</button>
        </div>
      </section>
  
      <!-- 性能参数 -->
      <section class="performance-params">
        <h2>性能参数</h2>
        <p>负载均衡，CDN调节，自动扩容</p>
      </section>
  
      <!-- 服务组件 -->
      <section class="service-components">
        <h2>服务组件</h2>
        <p>云电脑上各种服务的功能设置，网络配置等</p>
      </section>
  
      <!-- 性能加速 -->
      <section class="performance-acceleration">
        <h2>性能加速</h2>
        <p>分布式计算，加速设置</p>
      </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        statuses: [
          { label: 'Error', class: 'error', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
          { label: 'Running', class: 'running', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
          { label: 'Uploading', class: 'uploading', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
          { label: 'Downloading', class: 'downloading', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
          { label: 'Done', class: 'done', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
          { label: 'Stopped', class: 'stopped', icon: 'https://ide.code.fun/api/image?token=670d05920a3d780012a62bb2&name=d4972024bd8c5346f38423077f85111a.png' },
        ],
        osOptions: ['Windows', 'Linux', 'MacOS'],
        archOptions: ['arm', 'X86_64'],
        cloudProviders: ['Amazon', 'Azure', 'Ali Cloud'],
        nodes: [
          { id: 1, name: 'Azure/WS2', details: 'RTX4090 / 32GB' },
          { id: 2, name: 'Azure/WS2', details: 'GTX2080 / 16GB' },
        ],
        selectedOS: '',
        selectedArch: '',
        selectedCloud: '',
      };
    },
    methods: {
      selectOS(os) {
        this.selectedOS = os;
      },
      selectArch(arch) {
        this.selectedArch = arch;
      },
      selectCloud(provider) {
        this.selectedCloud = provider;
      },
      uploadYaml(event) {
        const file = event.target.files[0];
        console.log('Uploaded YAML file:', file);
      },
    },
  };
  </script>
  
  <style scoped>
  .dashboard {
    padding: 20px;
    font-family: Arial, sans-serif;
  }
  .status-bar {
    display: flex;
    gap: 15px;
    margin-bottom: 20px;
  }
  .status-btn {
    padding: 0;
    border-radius: 2.5rem;
    border: none;
    color: #fff;
    background: none;
  }
  .status-btn .page {
    display: flex;
    align-items: center;
    padding: 0.6rem 1.5rem;
    border-radius: 2.5rem;
    border: solid 0.25rem #ffffff;
    width: auto;
  }
  .status-btn.error .page {
    background-color: #ff6b6b;
  }
  .status-btn.running .page {
    background-color: #6c63ff;
  }
  .status-btn.uploading .page {
    background-color: #38bdf8;
  }
  .status-btn.downloading .page {
    background-color: #e879f9;
  }
  .status-btn.done .page {
    background-color: #34d399;
  }
  .status-btn.stopped .page {
    background-color: #a3a3a3;
  }
  .image-wrapper {
    padding: 0.13rem 0;
    background-color: transparent;
    border-radius: 50%;
    width: 2.5rem;
    height: 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .image {
    width: 2rem;
    height: 2rem;
  }
  .text {
    margin-left: 0.5rem;
    color: #ffffff;
    font-size: 1.25rem;
    font-family: Inder;
    line-height: 1.27rem;
  }
  section {
    margin-bottom: 20px;
    padding: 10px;
    border: 1px solid #f0f0f0;
    border-radius: 10px;
  }
  h2 {
    font-size: 16px;
    margin-bottom: 10px;
  }
  .env-container {
    display: flex;
    flex-direction: row;
    gap: 20px;
  }
  .env-menu {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  .menu-btn {
    padding: 10px;
    border: 1px solid #d9d9d9;
    background-color: #fff;
    color: #333;
    border-radius: 5px;
    cursor: pointer;
  }
  .menu-btn.active {
    background-color: #ffcccc;
  }
  .env-options {
    display: flex;
    flex-direction: column;
    gap: 15px;
  }
  .os-options,
  .arch-options {
    display: flex;
    gap: 10px;
  }
  .os-btn,
  .arch-btn {
    padding: 5px 15px;
    border: 1px solid #d9d9d9;
    border-radius: 5px;
    cursor: pointer;
  }
  .os-btn.active,
  .arch-btn.active {
    background-color: #ff8888;
    color: #fff;
  }
  .cloud-options,
  .node-options {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
  }
  .cloud-btn {
    padding: 5px 10px;
    border: 1px solid #d9d9d9;
    border-radius: 5px;
    cursor: pointer;
  }
  .cloud-btn.active {
    background-color: #1890ff;
    color: #fff;
  }
  .node {
    border: 1px solid #d9d9d9;
    padding: 10px;
    border-radius: 5px;
  }
  </style>