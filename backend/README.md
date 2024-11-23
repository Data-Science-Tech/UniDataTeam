# UniDataTeam

## 部分接口使用说明

**创建配置(/api/model-configs)**

后端在保存配置的同时会返回该配置相关的信息，前端可以取出model-config-id

```javascript
// 前端调用示例  
const response = await api.createModelConfig(configData);  
const configId = response.data.id; // 获取返回的配置id
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
