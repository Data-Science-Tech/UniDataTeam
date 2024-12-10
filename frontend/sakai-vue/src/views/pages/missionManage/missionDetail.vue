<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import GetAllTasksApi from '@/Api/GetAllTasksApi.js';
import Chart from 'primevue/chart'; // 添加图表组件

const route = useRoute();
const taskId = route.params.id;
const taskDetail = ref(null);
const trainingResult = ref(null);
const progress = ref(0);
let ws = null;

// 默认任务数据
const defaultTaskDetail = {
    id: '未知',
    algorithm: 'ResNet18',
    learningRate: 0.001,
    numEpochs: 10,
    batchSize: 32,
    momentumValue: 0.9,
    weightDecay: 0.0001
};

// 控制台日志
const consoleLogs = ref([]);
const maxLogs = 100; // 最大日志数量

// 添加日志
const addLog = (message, type = 'info') => {
    const log = {
        timestamp: new Date().toLocaleTimeString(),
        message,
        type, // info, error, warning, success
        id: Date.now()
    };
    consoleLogs.value.unshift(log);
    if (consoleLogs.value.length > maxLogs) {
        consoleLogs.value.pop();
    }
};

// 获取任务详情
const getTaskDetail = async () => {
    try {
        const response = await GetAllTasksApi.getalltests(1);
        const foundTask = response.data.find(task => task.id === parseInt(taskId));
        taskDetail.value = foundTask || defaultTaskDetail;
        addLog(`成功加载任务 ${taskId} 的详情`, 'success');
    } catch (error) {
        console.error('获取任务详情失败:', error);
        taskDetail.value = defaultTaskDetail;
        addLog(`加载任务详情失败: ${error.message}`, 'error');
    }
};

// 连接WebSocket获取进度
const lossChartData = ref({
    labels: [],
    datasets: [{
        label: '当前损失',
        data: [],
        borderColor: '#42A5F5',
        tension: 0.4,
        fill: false
    }, {
        label: '平均损失',
        data: [],
        borderColor: '#66BB6A',
        tension: 0.4,
        fill: false
    }]
});

// 图表配置
const chartOptions = {
    plugins: {
        legend: {
            labels: {
                color: '#eee'
            }
        }
    },
    scales: {
        y: {
            ticks: { color: '#eee' },
            grid: { color: 'rgba(255,255,255,0.1)' }
        },
        x: {
            ticks: { color: '#eee' },
            grid: { color: 'rgba(255,255,255,0.1)' }
        }
    }
};

const connectWebSocket = () => {
    try {
        if (ws) {
            ws.close();
        }
        
        ws = new WebSocket(`ws://localhost:8080/ws/training-progress/${taskId}`);
        
        ws.onopen = () => {
            addLog('WebSocket连接成功', 'success');
        };
        
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                // 更新进度
                progress.value = Math.round(data.progress_percentage);
                
                // 更新图表数据
                if (data.current_epoch && data.current_batch) {
                    const batchLabel = `E${data.current_epoch}-B${data.current_batch}`;
                    lossChartData.value.labels.push(batchLabel);
                    lossChartData.value.datasets[0].data.push(parseFloat(data.current_loss));
                    lossChartData.value.datasets[1].data.push(parseFloat(data.avg_loss));
                    
                    // 限制显示的数据点数量
                    const maxDataPoints = 20;
                    if (lossChartData.value.labels.length > maxDataPoints) {
                        lossChartData.value.labels = lossChartData.value.labels.slice(-maxDataPoints);
                        lossChartData.value.datasets[0].data = lossChartData.value.datasets[0].data.slice(-maxDataPoints);
                        lossChartData.value.datasets[1].data = lossChartData.value.datasets[1].data.slice(-maxDataPoints);
                    }
                    
                    // 强制更新图表
                    lossChartData.value = { ...lossChartData.value };
                }
                
                // 添加日志
                addLog(`Epoch: ${data.current_epoch}/${data.total_epochs} | Batch: ${data.current_batch}/${data.total_batches} | Loss: ${parseFloat(data.current_loss).toFixed(4)}`, 'info');
                
                // 如果训练完成，获取结果
                if (progress.value >= 100) {
                    getTrainingResults();
                }
            } catch (error) {
                addLog(`解析WebSocket数据失败: ${error.message}`, 'error');
            }
        };

        ws.onerror = (error) => {
            addLog(`WebSocket错误: ${error}`, 'error');
        };

        ws.onclose = () => {
            addLog('WebSocket连接已关闭', 'warning');
        };

    } catch (error) {
        addLog(`建立WebSocket连接失败: ${error.message}`, 'error');
    }
};

// 获取训练结果
const getTrainingResults = async () => {
    try {
        const response = await fetch(`http://localhost:8080/api/training-results/${taskId}`);
        if (!response.ok) throw new Error('获取训练结果失败');
        const data = await response.json();
        trainingResult.value = data;
        addLog('成功获取训练结果', 'success');
    } catch (error) {
        addLog(`获取训练结果失败: ${error.message}`, 'error');
    }
};

// 下载训练日志
const downloadLogs = async () => {
    try {
        const response = await fetch(`http://localhost:8080/api/training-results/logs/${taskId}`);
        if (!response.ok) throw new Error('下载日志失败');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `training-log-${taskId}.txt`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        addLog('成功下载训练日志', 'success');
    } catch (error) {
        addLog(`下载日志失败: ${error.message}`, 'error');
    }
};

onMounted(() => {
    getTaskDetail();
    connectWebSocket();
    getTrainingResults();
});

onBeforeUnmount(() => {
    if (ws) {
        ws.close();
    }
});

const isConsoleOpen = ref(false);
const consoleHeight = ref('400px');

const toggleConsole = () => {
    isConsoleOpen.value = !isConsoleOpen.value;
};
</script>

<template>
    <div class="grid">
        <!-- 任务基本信息 -->
        <div class="col-12">
            <div class="card">
                <h2 class="text-2xl font-bold mb-4">任务详情</h2>
                <DataTable v-if="taskDetail" :value="[taskDetail]" tableStyle="min-width: 50rem">
                    <Column field="id" header="任务ID"></Column>
                    <Column field="algorithm" header="算法"></Column>
                    <Column field="learningRate" header="学习率"></Column>
                    <Column field="numEpochs" header="训练轮次"></Column>
                    <Column field="batchSize" header="批次大小"></Column>
                    <Column field="momentumValue" header="动量值"></Column>
                    <Column field="weightDecay" header="权重衰减"></Column>
                </DataTable>
            </div>
        </div>

        <!-- 训练进度和实时图表 -->
        <div class="col-12 lg:col-8">
            <div class="grid">
                <!-- 训练进度 -->
                <div class="col-12">
                    <div class="card">
                        <h3 class="text-xl font-bold mb-4">训练进度</h3>
                        <div class="training-progress">
                            <ProgressBar :value="progress" />
                            <div class="progress-stats mt-3">
                                <div class="stat-item">
                                    <i class="pi pi-percentage"></i>
                                    <span>{{ progress.toFixed(2) }}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 损失值图表 -->
                <div class="col-12">
                    <div class="card">
                        <h3 class="text-xl font-bold mb-4">训练损失值趋势</h3>
                        <Chart type="line" 
                               :data="lossChartData" 
                               :options="chartOptions" 
                               class="loss-chart" />
                    </div>
                </div>
            </div>
        </div>

        <!-- 训练结果 -->
        <div class="col-12 lg:col-4">
            <div class="card h-full">
                <h3 class="text-xl font-bold mb-4">训练结果</h3>
                <div v-if="trainingResult" class="training-results">
                    <div class="p-2 result-item">
                        <i class="pi pi-calendar mr-2"></i>
                        <strong>开始时间:</strong> 
                        <span>{{ new Date(trainingResult.startTime).toLocaleString() }}</span>
                    </div>
                    <div class="p-2">
                        <strong>结束时间:</strong> {{ new Date(trainingResult.endTime).toLocaleString() }}
                    </div>
                    <div class="p-2">
                        <strong>最终损失值:</strong> {{ trainingResult.finalLoss }}
                    </div>
                    <div class="p-2">
                        <strong>准确率:</strong> {{ trainingResult.accuracy }}
                    </div>
                    <div class="p-2">
                        <strong>训练日志路径:</strong> {{ trainingResult.trainingLogs }}
                    </div>
                    <div class="p-2">
                        <strong>模型文件路径:</strong> {{ trainingResult.modelFilePath }}
                    </div>
                    <Button label="下载训练日志" icon="pi pi-download" @click="downloadLogs" />
                </div>
            </div>
        </div>

        <!-- 控制台抽屉 -->
        <div class="console-drawer" :class="{ 'console-open': isConsoleOpen }" :style="{ 'z-index': isConsoleOpen ? '1000' : '999' }">
            <div class="console-toggle" @click="toggleConsole">
                <i :class="['pi', isConsoleOpen ? 'pi-chevron-down' : 'pi-chevron-up']"></i>
                控制台
                <span class="log-count">{{ consoleLogs.length }}</span>
            </div>
            <div class="console-content">
                <div class="card console-card glass-effect">
                    <div class="console-header">
                        <div class="header-left">
                            <h3 class="text-xl font-bold mb-0">
                                <i class="pi pi-terminal mr-2"></i>控制台输出
                            </h3>
                            <div class="console-stats">
                                <span class="stat-item">
                                    <i class="pi pi-clock"></i> {{ consoleLogs.length }}条日志
                                </span>
                            </div>
                        </div>
                        <div class="header-actions">
                            <Button icon="pi pi-filter" 
                                   class="p-button-rounded p-button-text" 
                                   tooltip="过滤日志" />
                            <Button icon="pi pi-trash" 
                                   class="p-button-rounded p-button-text" 
                                   @click="consoleLogs = []" 
                                   tooltip="清空控制台" />
                        </div>
                    </div>
                    <div class="console-container custom-scrollbar">
                        <TransitionGroup name="log-list" tag="div" appear>
                            <div v-for="log in consoleLogs" 
                                 :key="log.id" 
                                 :class="['console-line', `console-${log.type}`, 'glass-effect-light']">
                                <div class="log-content">
                                    <span class="console-timestamp">
                                        <i class="pi pi-clock mr-1"></i>
                                        {{ log.timestamp }}
                                    </span>
                                    <span :class="['console-type-badge', `type-${log.type}`]">
                                        {{ log.type }}
                                    </span>
                                    <span class="console-message">{{ log.message }}</span>
                                </div>
                                <div class="log-actions">
                                    <i class="pi pi-copy action-icon" title="复制"></i>
                                </div>
                            </div>
                        </TransitionGroup>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.glass-effect {
    backdrop-filter: blur(10px);
    background: rgba(14, 14, 18, 0.95) !important; /* 加深背景色并提高不透明度 */
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

.glass-effect-light {
    background: rgba(30, 30, 35, 0.7) !important; /* 调整日志条目背景色 */
    border: 1px solid rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(5px);
}

.console-card {
    color: #e0e0e0;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    border-radius: 12px;
    overflow: hidden;
    background: #1a1a1a !important; /* 确保主背景色 */
}

.console-header {
    padding: 1.25rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.console-stats {
    display: flex;
    gap: 1rem;
    margin-left: 1rem;
}

.stat-item {
    font-size: 0.9rem;
    color: #bababa;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.header-actions {
    display: flex;
    gap: 0.5rem;
}

.console-container {
    height: 400px;
    overflow-y: auto;
    padding: 1rem;
    background: rgba(14, 14, 18, 0.95) !important; /* 确保滚动区域背景色 */
}

.console-line {
    padding: 0.75rem;
    margin: 0.5rem 0;
    border-radius: 8px;
    transition: all 0.3s ease;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: relative;
    overflow: hidden;
    background: rgba(30, 30, 35, 0.7) !important; /* 确保日志条目背景色 */
}

.console-line:hover {
    transform: translateX(5px);
    background: rgba(40, 40, 45, 0.8) !important; /* 调整悬停时的背景色 */
}

.log-content {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.console-timestamp {
    color: #666;
    font-size: 0.9rem;
    min-width: 100px;
    display: flex;
    align-items: center;
}

.console-type-badge {
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
    font-size: 0.8rem;
    text-transform: uppercase;
    font-weight: bold;
    min-width: 80px;
    text-align: center;
}

/* 修改类型标签的样式 */
.type-info { 
    background: rgba(32, 156, 238, 0.15); 
    color: #20a0ff; 
}
.type-error { 
    background: rgba(245, 108, 108, 0.15); 
    color: #ff6b6b; 
}
.type-warning { 
    background: rgba(255, 217, 61, 0.15); 
    color: #ffd93d; 
}
.type-success { 
    background: rgba(107, 255, 107, 0.15); 
    color: #6bff6b; 
}

.console-message {
    font-size: 0.95rem;
    line-height: 1.5;
}

.log-actions {
    opacity: 0;
    transition: opacity 0.3s ease;
}

.console-line:hover .log-actions {
    opacity: 1;
}

.action-icon {
    color: #666;
    cursor: pointer;
    padding: 0.5rem;
    border-radius: 4px;
    transition: all 0.3s ease;
}

.action-icon:hover {
    color: #fff;
    background: rgba(255, 255, 255, 0.1);
}

/* 动画���果增强 */
.log-list-enter-active {
    transition: all 0.4s ease-out;
}

.log-list-leave-active {
    transition: all 0.3s ease-in;
    position: absolute;
    width: 100%;
}

.log-list-enter-from {
    opacity: 0;
    transform: translateX(-30px);
}

.log-list-leave-to {
    opacity: 0;
    transform: translateX(30px);
}

/* 自定义滚动条 */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 3px;
    transition: background 0.3s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}

@keyframes glow {
    0% { box-shadow: 0 0 5px rgba(0, 0, 0, 0.3); }
    50% { box-shadow: 0 0 20px rgba(0, 0, 0, 0.5); }
    100% { box-shadow: 0 0 5px rgba(0, 0, 0, 0.3); }
}

.console-card {
    animation: glow 3s infinite;
}

/* 调整按钮样式 */
.header-actions :deep(.p-button.p-button-text) {
    color: #888 !important;
}

.header-actions :deep(.p-button.p-button-text:hover) {
    color: #fff !important;
    background: rgba(255, 255, 255, 0.1) !important;
}

/* 增加深色主题兼容 */
:deep(.p-tooltip) {
    background: rgba(14, 14, 18, 0.95);
    color: #e0e0e0;
}

.training-progress {
    padding: 1rem;
}

.progress-stats {
    display: flex;
    justify-content: center;
    gap: 2rem;
}

.progress-stats .stat-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: #666;
}

.loss-chart {
    min-height: 300px;
    width: 100%;
    position: relative;
}

/* 控制台抽屉样式 */
.console-drawer {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(14, 14, 18, 0.95);
    box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.2);
    transform: translateY(calc(100% - 40px));
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.console-drawer.console-open {
    transform: translateY(0);
}

.console-toggle {
    height: 40px;
    background: rgba(14, 14, 18, 0.95);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    padding: 0 1rem;
    cursor: pointer;
    color: #e0e0e0;
    font-weight: 500;
    gap: 0.5rem;
    backdrop-filter: blur(10px);
}

.console-toggle:hover {
    background: rgba(20, 20, 25, 0.95);
}

.console-toggle i {
    transition: transform 0.3s ease;
}

.console-open .console-toggle i {
    transform: rotate(180deg);
}

.log-count {
    background: rgba(255, 255, 255, 0.1);
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    margin-left: 0.5rem;
}

.console-content {
    height: calc(100vh - 40px - 64px); /* 减去顶部导航和控制台按钮的高度 */
    max-height: 50vh;
}

.console-card {
    border-radius: 0;
    height: 100%;
}

/* 调整主内容区域，为控制台留出空间 */
.grid {
    padding-bottom: 40px; /* 只预留控制台按钮的高度 */
    min-height: calc(100vh - 40px);
    position: relative;
}

/* 优化训练结果展示 */
.training-results {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.result-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.02);
    border-radius: 6px;
}

.result-item:hover {
    background: rgba(255, 255, 255, 0.05);
}

/* 响应式调整 */
@media screen and (max-width: 991px) {
    .grid {
        padding-bottom: 440px;
    }
}
</style>
