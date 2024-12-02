# UniDataTeam

## 部分接口使用说明

### 普通接口

**创建模型配置 (/api/model-configs)**

请求方式：POST

请求头：
```http
Content-Type: application/json
```

请求体：
```json
{
    "algorithm": "FAST_R_CNN",
    "learningRate": 0.001,
    "numEpochs": 100,
    "batchSize": 32,
    "momentumValue": 0.9,
    "weightDecay": 0.0005,
    "sceneIds": [1, 2, 3]
}
```

字段说明：
| 字段名 | 类型 | 必填 | 说明 |
|-------|------|-----|------|
| algorithm | String | 是 | 算法名称 |
| learningRate | Double | 是 | 学习率 |
| numEpochs | Integer | 是 | 训练轮次 |
| batchSize | Integer | 是 | 批次大小 |
| momentumValue | Double | 是 | 动量值 |
| weightDecay | Double | 是 | 权重衰减 |
| sceneIds | Integer[] | 是 | 场景ID列表 |

响应示例：
```json
{
    "id": 1,
    "algorithm": "FAST_R_CNN",
    "learningRate": 0.001,
    "numEpochs": 100,
    "batchSize": 32,
    "momentumValue": 0.9,
    "weightDecay": 0.0005,
    "scenes": [
        {
            "sceneId": 1,
            "sceneName": "交通场景"
        },
        {
            "sceneId": 2,
            "sceneName": "室内场景"
        }
    ]
}
```

响应字段说明：
| 字段名 | 类型 | 说明 |
|-------|------|------|
| id | Long | 配置ID |
| algorithm | String | 算法名称 |
| learningRate | Double | 学习率 |
| numEpochs | Integer | 训练轮次 |
| batchSize | Integer | 批次大小 |
| momentumValue | Double | 动量值 |
| weightDecay | Double | 权重衰减 |
| scenes | Object[] | 关联场景列表 |
| scenes.sceneId | Integer | 场景ID |
| scenes.sceneName | String | 场景名称 |

前端调用示例：
```javascript
// 创建配置数据
const configData = {
    algorithm: "FAST_R_CNN",
    learningRate: 0.001,
    numEpochs: 100,
    batchSize: 32,
    momentumValue: 0.9,
    weightDecay: 0.0005,
    sceneIds: [1, 2]
};

try {
    // 发送创建请求
    const response = await api.post('/api/model-configs', configData);
    
    // 获取返回的配置ID
    const configId = response.data.id;
    
    // 获取关联的场景信息
    const scenes = response.data.scenes;
    
    console.log('配置创建成功，ID:', configId);
    console.log('关联场景:', scenes);
} catch (error) {
    console.error('配置创建失败:', error);
}
```

说明：
1. 接口会验证所有必填字段
2. sceneIds中的场景ID必须是已存在的
3. 返回的数据包含完整的配置信息，包括关联的场景详情
4. 如果创建失败，将返回相应的错误信息

错误响应示例：
```json
{
    "timestamp": "2024-01-25T10:30:15.123+00:00",
    "status": 400,
    "error": "Bad Request",
    "message": "验证失败",
    "errors": [
        {
            "field": "algorithm",
            "message": "算法名称不能为空"
        },
        {
            "field": "sceneIds",
            "message": "至少需要选择一个场景"
        }
    ]
}
```




**获取训练结果(/api/training-results/logs/{trainingResultId})**

返回的结果是一个列表，因此需要注意指定数组中的元素

```javascript
// 获取某个模型配置的所有训练结果  
const response = await axios.get(`/api/training-results/by-config/${modelConfigId}`);  
const trainingResults = response.data; // 训练结果列表
```

```javascript
// 获取第一个训练结果的id  
const firstResultId = response.data[0].id;  

// 如果要获取所有训练结果的id，可以使用map  
const allIds = response.data.map(result => result.id);  

// 遍历所有训练结果  
response.data.forEach(result => {  
    console.log(result.id);  // 打印每个训练结果的id  
    console.log(result.startTime);  // 打印每个训练结果的开始时间  
    // ... 其他属性  
});
```

### WebSocket接口

**实时获取训练进度(ws://localhost:8080/ws/training-progress/{config_id})**

```javascript
// 建立WebSocket连接  
const ws = new WebSocket('ws://localhost:8080/ws/training-progress/16');  

// 接收消息  
ws.onmessage = (event) => {  
    const data = JSON.parse(event.data);  
    if (data.type === 'progress') {  
        console.log('训练进度:', data.progress_percentage + '%');  
        console.log('当前轮次:', data.current_epoch + '/' + data.total_epochs);  
        console.log('当前损失:', data.current_loss);  
    }  
};  

// 连接建立  
ws.onopen = () => {  
    console.log('连接已建立');  
};  

// 连接关闭  
ws.onclose = () => {  
    console.log('连接已关闭');  
};
```

