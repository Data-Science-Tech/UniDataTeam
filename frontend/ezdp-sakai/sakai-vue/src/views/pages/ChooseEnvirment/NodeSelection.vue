<template>
    <div class="node-selection-page">
        <!-- 标题部分 -->
        <div class="title">
            节点选择
        </div>

        <!-- 云服务选择按钮 -->
        <div class="cloud-providers">
            <button class="provider-button active">Amazon</button>
            <button class="provider-button">Azure</button>
            <button class="provider-button">Ali cloud</button>
        </div>

        <!-- 标签选择 -->
        <div class="tag-selection">
            <button class="tag-button">CPU</button>
            <button class="tag-button active">GPU</button>
            <button class="tag-button">INF2</button>
        </div>

        <!-- 云服务器列表 -->
        <div class="server-list">
            <div v-for="server in servers" :key="server.id" class="server-card">
                <div class="server-icon">
                    <!-- 图标可以替换为实际图片 -->
                    <span>💬</span>
                </div>
                <div class="server-info">
                    <div class="server-name">{{ server.name }}</div>
                    <div class="server-config">{{ server.config }}</div>
                    <div class="server-price">{{ server.price }}/h</div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
const servers = [
    { id: 1, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
    { id: 2, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
    { id: 3, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
    { id: 4, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
    { id: 5, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
    { id: 6, name: "Azune/US123", config: "RTX4090 | 32GB", price: "0.6$" },
];
</script>

<style scoped>
/* 页面容器 */
.node-selection-page {
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: height 0.3s ease-in-out;
}

/* 标题部分样式 */
.title {
    font-size: 35px;
    font-weight: bold;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
}

.title::before {
    content: '';
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ff6666;
    margin-right: 10px;
}

/* 云服务提供商按钮组样式 */
.cloud-providers {
    display: flex;
    justify-content: space-between;
    margin-bottom: 15px;
}

.provider-button {
    flex: 1;
    padding: 10px;
    margin: 0 5px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: #f2f2f2;
    cursor: pointer;
    font-weight: bold;
}

.provider-button.active {
    background-color: #ffb3b3;
}

/* 标签选择部分 */
.tag-selection {
    display: flex;
    margin-bottom: 20px;
}

.tag-button {
    padding: 10px 20px;
    border: 1px solid #e0e0e0;
    border-radius: 20px;
    background-color: #f2f2f2;
    margin-right: 10px;
    cursor: pointer;
}

.tag-button.active {
    background-color: #ff9999;
    color: white;
}

/* 云服务器卡片列表 */
.server-list {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

.server-card {
    width: 30%;
    margin-bottom: 20px;
    background-color: #fff;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.server-icon {
    font-size: 40px;
    margin-right: 10px;
}

.server-info {
    text-align: left;
}

.server-name {
    font-size: 14px;
    font-weight: bold;
}

.server-config {
    font-size: 12px;
    color: #999;
}

.server-price {
    font-size: 14px;
    color: #ff6666;
}
</style>