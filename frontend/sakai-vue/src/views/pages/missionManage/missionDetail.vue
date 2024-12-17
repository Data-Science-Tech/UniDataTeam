<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import GetAllTasksApi from '@/Api/GetAllTasksApi.js';
import Chart from 'primevue/chart'; // 添加图表组件

import TaskProcessInfo from '@/Api/TaskProcessInfo.js';
import GetTrainingResults from '@/Api/GetTrainingResults';
import GetTrainingResultLogs from '@/Api/GetTrainingResultLogs';

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
    weightDecay: 0.0001,
    status: 'UNKNOWN',
    resultId: '未知',
    startTime: '未知',
    endTime: '未知',
    finalLoss: '未知',
    accuracy: '未知',
    trainingLogs: '未知',
    modelFilePath: '未知'
};



// 控制台日志
const consoleLogs = ref([]);
const maxLogs = 1000; // 最大日志数量

// 添加日志
const addLog = (message, type = 'info', isDebug = false) => {
    const log = {
        timestamp: new Date().toLocaleTimeString(),
        message: isDebug ? `[Debug] ${message}` : message,
        type: isDebug ? 'debug' : type,
        id: Date.now()
    };
    consoleLogs.value.unshift(log);
    if (consoleLogs.value.length > maxLogs) {
        consoleLogs.value.pop();
    }
};

// 添加任务状态变量
const taskStatus = ref('pending'); // 'pending', 'completed', 'failed'
const receivedResults = new Set(); // 用于追踪已接收的结果

// 获取任务详情
const getTaskDetail = async () => {
    try {
        addLog('开始获取任务详情: ' + taskId, 'info', false);
        const response = await GetAllTasksApi.getalltests(1);
        addLog('API响应数据: ' + JSON.stringify(response.data).slice(0, 200) + '...', 'debug', true);
        const foundTask = response.data.find(task => task.id === parseInt(taskId));
        
        if (foundTask) {
            taskDetail.value = foundTask;
            addLog('成功解析任务数据', 'success', false);
            await checkTaskStatus();
        } else {
            addLog('未找到任务，使用默认值', 'warning', false);
            taskDetail.value = defaultTaskDetail;
        }
    } catch (error) {
        addLog(`获取任务详情失败: ${error.message}`, 'error', false);
        taskDetail.value = defaultTaskDetail;
    }
};

// 修改检查任务状态的方法
const checkTaskStatus = async () => {
    try {
        addLog('开始检查任务状态', 'info', false);
        
        const status = taskDetail.value.status;
        addLog(`任务状态: ${status}`, 'debug', true);

        if (status === 'COMPLETED') {
            addLog('任务已完成，准备获取历史数据', 'debug', false);
            taskStatus.value = 'completed';
            await getHistoricalData();
        } else if (status === 'FAILED') {
            taskStatus.value = 'failed';
            addLog('任务执行失败', 'error', false);
        } else if (status === 'RUNNING'){
            addLog('任务进行中', 'info', false);
            taskStatus.value = 'running';
            updateProcessData();//实时获取数据
        } else {
            addLog('任务状态未知', 'unknown', false);
            taskStatus.value = 'pending';
        }
    } catch (error) {
        addLog(`检查任务状态失败: ${error.message}`, 'error', false);
    }
};

const updateChartData = (data) => {
    try {
        addLog('更新图表数据', 'debug', true);

        const label = `E${data.currentEpoch}-B${data.currentBatch}`;

        // 创建新数据对象，确保不会修改原有响应式引用
        const newLabels = [...lossChartData.value.labels, label];
        const newCurrentLossData = [...lossChartData.value.datasets[0].data, data.currentLoss];
        const newAvgLossData = [...lossChartData.value.datasets[1].data, data.avgLoss];

        // 限制数据点数量为100
        if (newLabels.length > 100) {
            newLabels.shift();
            newCurrentLossData.shift();
            newAvgLossData.shift();
        }

        // 重新赋值响应式对象
        lossChartData.value = {
            labels: newLabels,
            datasets: [
                {
                    label: '当前损失',
                    data: newCurrentLossData,
                    borderColor: '#42A5F5',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: '平均损失',
                    data: newAvgLossData,
                    borderColor: '#66BB6A',
                    tension: 0.4,
                    fill: false
                }
            ]
        };

        // 手动触发图表更新
        if (typeof chart !== 'undefined' && chart.value) {
            chart.value.update('none');
        }

        addLog(`图表已更新: 当前损失=${data.currentLoss.toFixed(4)}, 平均损失=${data.avgLoss.toFixed(4)}`, 'debug', false);
    } catch (error) {
        addLog(`更新图表数据失败: ${error.message}`, 'error', false);
    }
};



// 任务状态检查函数
const checkTaskStatusForUpdate = async () => {
    try {
        const response = await GetAllTasksApi.getalltests(1);
        const currentTask = response.data.find(task => task.id === parseInt(taskId));
        
        if (!currentTask) {
            addLog('未找到当前任务', 'error', false);
            return false;
        }

        if (currentTask.status === 'COMPLETED') {
            addLog('任务已完成，准备获取历史数据', 'debug', true);
            taskStatus.value = 'completed';
            await getHistoricalData();
            return false;
        } else if (currentTask.status === 'FAILED') {
            addLog('任务执行失败', 'error', false);
            taskStatus.value = 'failed';
            return false;
        }
        
        return true;
    } catch (error) {
        addLog(`检查任务状态失败: ${error.message}`, 'error', false);
        return false;
    }
};

// 处理训练数据的函数
const processTrainingData = async () => {
    try {
        const response = await TaskProcessInfo.getTaskProcessInfo(taskId);
        const data = response.data;
        
        if (!Array.isArray(data) || data.length === 0) {
            addLog('没有新的训练数据', 'warning', true);
            return;
        }

        // 获取最新的数据点
        const latestData = data[data.length - 1];
        
        // 更新进度条
        progress.value = latestData.progressPercentage;
        
        // 更新图表
        updateChartData(latestData);
        
        addLog(`进度更新: ${progress.value}%, 当前epoch: ${latestData.currentEpoch}/${latestData.totalEpochs}`, 'info', false);
        
    } catch (error) {
        addLog(`处理训练数据失败: ${error.message}`, 'error', true);
    }
};

// 实时获取流程控制函数
const updateProcessData = async () => {
    let isTaskActive = true;

    const checkStatus = async () => {
        if (!isTaskActive) return;
        const shouldContinue = await checkTaskStatusForUpdate();
        if (shouldContinue) {
            await processTrainingData();
            addLog('尝试获取训练数据', 'info', false);
            setTimeout(checkStatus, 10000); // 每10秒获取一次数据
        }
    };

    const monitorStatus = async () => {
        if (!isTaskActive) return;
        const shouldContinue = await checkTaskStatusForUpdate();
        if (shouldContinue) {
            setTimeout(monitorStatus, 5000); // 每5秒检查一次状态
        }
    };

    try {
        checkStatus();
        monitorStatus();

        // 设置超时保护
        setTimeout(() => {
            isTaskActive = false;
            addLog('数据更新超时停止', 'warning', false);
        }, 3600000); // 1小时后自动停止
    } catch (error) {
        isTaskActive = false;
        addLog(`更新进度数据失败: ${error.message}`, 'error', false);
    }
};

// 修改updateChartWithHistoricalData函数
const updateChartWithHistoricalData = (data) => {
    try {
        addLog('开始处理历史训练数据', 'info', false);
        
        // 设置进度为100%，因为这是历史数据
        progress.value = 100;
        
        // 准备图表数据
        const labels = [];
        const currentLossData = [];
        const avgLossData = [];
        
        // 处理每个数据点
        data.forEach((point) => {
            // 创建标签：Epoch-Batch格式
            const label = `E${point.currentEpoch}-B${point.currentBatch}`;
            labels.push(label);
            
            // 收集损失值数据
            currentLossData.push(point.currentLoss);
            avgLossData.push(point.avgLoss);
        });
        
        // 更新图表数据
        lossChartData.value = {
            labels: labels,
            datasets: [
                {
                    label: '当前损失',
                    data: currentLossData,
                    borderColor: '#42A5F5',
                    tension: 0.4,
                    fill: false
                },
                {
                    label: '平均损失',
                    data: avgLossData,
                    borderColor: '#66BB6A',
                    tension: 0.4,
                    fill: false
                }
            ]
        };
        
        addLog('图表数据更新完成', 'success', true);
        addLog(`共处理 ${data.length} 个数据点`, 'info', true);
        
        // 由于是历史数据，将任务状态设置为已完成
        taskStatus.value = 'completed';
        
    } catch (error) {
        addLog(`处理历史数据失败: ${error.message}`, 'error', true);
    }
};

// 修改获取历史数据的方法
const getHistoricalData = async () => {
    try {
        const response = await TaskProcessInfo.getTaskProcessInfo(taskId);
        const data = response.data;
        
        // 更新图表和进度
        updateChartWithHistoricalData(data);
        getTrainingResults();
        
        addLog('已加载历史训练数据', 'success', false);
    } catch (error) {
        addLog(`获取历史数据失败: ${error.message}`, 'error', false);
    }
};

// 图表数据
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

// // 修改WebSocket消息处理逻辑
// const handleWebSocketMessage = (data) => {
//     const resultKey = `${data.current_epoch}-${data.current_batch}`;
    
//     if (!receivedResults.has(resultKey)) {
//         receivedResults.add(resultKey);
//         addLog(`处理新的训练数据: Epoch ${data.current_epoch}, Batch ${data.current_batch}`, 'debug', true);
        
//         progress.value = Math.round(data.progress_percentage);
//         addLog(`当前进度: ${progress.value}%`, 'info', true);
        
//         if (data.current_epoch && data.current_batch) {
//             addLog(`更新损失值数据: ${parseFloat(data.current_loss).toFixed(4)}`, 'debug', true);
//             updateChartData(data);
//         }
        
//         if (progress.value >= 100) {
//             addLog('训练完成，正在关闭连接...', 'success', true);
//             taskStatus.value = 'completed';
//             if (ws) {
//                 ws.close();
//                 ws = null;
//             }
//             getTrainingResults();
//         }
//     } else {
//         addLog(`跳过重复数据: ${resultKey}`, 'debug', true);
//     }
// };

// // 修改WebSocket连接逻辑
// const connectWebSocket = () => {
//     if (taskStatus.value === 'completed') {
//         addLog('任务已完成，无需建立连接', 'info', true);
//         return;
//     }
    
//     try {
//         if (ws) {
//             addLog('关闭现有WebSocket连接', 'warning', true);
//             ws.close();
//         }
        
//         addLog(`正在连接WebSocket: ${taskId}`, 'info', true);
//         ws = new WebSocket(`ws://localhost:8080/ws/training-progress/${taskId}`);
        
//         ws.onopen = () => {
//             addLog('WebSocket连接建立成功', 'success', false);
//         };
        
//         ws.onmessage = (event) => {
//             try {
//                 const data = JSON.parse(event.data);
//                 handleWebSocketMessage(data);
//             } catch (error) {
//                 addLog(`解析WebSocket数据失败: ${error.message}`, 'error');
//             }
//         };

//         ws.onerror = (error) => {
//             console.error('[Debug] WebSocket错误:', error);
//             addLog(`WebSocket错误: ${error}`, 'error');
//         };

//         ws.onclose = () => {
//             console.log('[Debug] WebSocket连接已关闭');
//             addLog('WebSocket连接已关闭', 'warning');
//         };

//     } catch (error) {
//         addLog(`WebSocket连接失败: ${error.message}`, 'error', true);
//     }
// };

// 获取训练结果
const getTrainingResults = async () => {
    try {
        const response = await GetTrainingResults.getTrainingResults(taskId);
        const data = await response.data;
        trainingResult.value = data;
        addLog('成功获取训练结果', 'success');

        defaultTaskDetail.resultId = trainingResult.value[0].id; // 使用训练结果中的id
        defaultTaskDetail.startTime = trainingResult.value[0].startTime;
        defaultTaskDetail.endTime = trainingResult.value[0].endTime;
        defaultTaskDetail.accuracy = trainingResult.value[0].accuracy;
        defaultTaskDetail.finalLoss = trainingResult.value[0].finalLoss;
        defaultTaskDetail.trainingLogs = trainingResult.value[0].trainingLogs;
        defaultTaskDetail.modelFilePath = trainingResult.value[0].modelFilePath;
        //console.log('训练结果ID', resultId);
        addLog(`训练结果ID:${defaultTaskDetail.resultId}`, 'debug', true);
        addLog(`训练开始时间:${defaultTaskDetail.startTime}`, 'debug', true);
    
    } catch (error) {
        addLog(`获取训练结果失败: ${error.message}`, 'error');
        addLog(`训练结果ID:${trainingResult.value}`, 'error', false);
    }
};

// 下载训练日志
const downloadLogs = async () => {
    try {
        if (!trainingResult.value || !trainingResult.value[0].id) {
            addLog('没有可用的训练结果ID', 'error');
            return;
        }

        const trainingResultId = trainingResult.value[0].id;
        const response = await GetTrainingResultLogs.getTrainingResultLogs(trainingResultId);
        //addLog(`训练log: ${response}`, 'debug');
        //console.log('训练log', response);

        if (response.status !== 200) throw new Error('下载日志失败');

        const blob = new Blob([response.data], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `training-log-${trainingResult.value[0].id}.txt`;
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
    addLog(`组件挂载，任务ID: ${taskId}`, 'Debug', true);
    getTaskDetail();
});

onBeforeUnmount(() => {
    addLog('组件即将卸载', 'Debug', true);
    // if (ws) {
    //     addLog('关闭WebSocket连接', 'Debug', true);
    //     ws.close();
    // }
    // 确保在组件卸载时停止所有定时器
    isTaskActive = false;
});

const isConsoleOpen = ref(true);
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
                    <div class="p-2">
                        <strong>开始时间:</strong> {{ defaultTaskDetail.startTime}}
                    </div>
                    <div class="p-2">
                        <strong>结束时间:</strong> {{ defaultTaskDetail.endTime }}
                    </div>
                    <div class="p-2">
                        <strong>最终损失值:</strong> {{ defaultTaskDetail.finalLoss }}
                    </div>
                    <div class="p-2">
                        <strong>准确率:</strong> {{ defaultTaskDetail.accuracy }}
                    </div>
                    <div class="p-2">
                        <strong>训练日志路径:</strong> {{ defaultTaskDetail.trainingLogs }}
                    </div>
                    <div class="p-2">
                        <strong>模型文件路径:</strong> {{ defaultTaskDetail.modelFilePath }}
                    </div>
                    <Button label="下载训练日志" icon="pi pi-download" @click="downloadLogs" />
                </div>
            </div>
        </div>

        <!-- 控制台抽屉 -->
        <div class="console-drawer" :class="{ 'console-open': isConsoleOpen }" :style="{ 'z-index': isConsoleOpen ? '1000' : '999' }">
            <div class="console-toggle" @click="toggleConsole">
                <i :class="['pi', isConsoleOpen ? 'pi-chevron-up' : 'pi-chevron-down']" </i>
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
.type-debug { 
    background: rgba(147, 147, 147, 0.15); 
    color: #93c5fd; 
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

/* 动画效果增强 */
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
